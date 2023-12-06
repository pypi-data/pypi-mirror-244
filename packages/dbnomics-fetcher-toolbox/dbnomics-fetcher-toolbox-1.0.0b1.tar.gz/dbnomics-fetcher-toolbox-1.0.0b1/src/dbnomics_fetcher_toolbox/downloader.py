import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, Final, Literal, TypeVar, overload

import daiquiri
from contexttimer import Timer
from returns.maybe import Maybe, Nothing, Some

from dbnomics_fetcher_toolbox._internal.argparse_utils import AnyId
from dbnomics_fetcher_toolbox._internal.file_utils import (
    create_directory,
    format_file_path_with_size,
    move_file,
)
from dbnomics_fetcher_toolbox._internal.formatting_utils import format_csv_values, format_timer
from dbnomics_fetcher_toolbox._internal.reports import DownloadReport
from dbnomics_fetcher_toolbox.download_cli import DownloadCLIArgs
from dbnomics_fetcher_toolbox.errors.downloader import (
    DuplicateResource,
    DuplicateResourceGroup,
    GroupAbortedAfterResourceSkipped,
    ResourceLoadError,
    ResourceSkipped,
)
from dbnomics_fetcher_toolbox.resource import Resource
from dbnomics_fetcher_toolbox.resource_group import ResourceGroup
from dbnomics_fetcher_toolbox.sources.base import Source
from dbnomics_fetcher_toolbox.types import ResourceFullId, ResourceGroupId

if TYPE_CHECKING:
    from dbnomics_fetcher_toolbox.serializers.base import Serializer

__all__ = ["Downloader"]


# TODO bring tools for incremental mode


logger = daiquiri.getLogger(__name__)


DEFAULT_CACHE_DIR_NAME: Final = "cache"
DEFAULT_DEBUG_DIR_NAME: Final = "debug-data"


T = TypeVar("T")


class Downloader(ABC):
    def __init__(self, *, args: DownloadCLIArgs) -> None:
        cache_dir = args.cache_dir
        if cache_dir is None:
            cache_dir = Path(DEFAULT_CACHE_DIR_NAME)
        self._cache_dir = cache_dir

        debug_dir = args.debug_dir
        if debug_dir is None:
            debug_dir = Path(DEFAULT_DEBUG_DIR_NAME)
        self._debug_dir = debug_dir

        self._excluded = args.exclude
        self._fail_fast = args.fail_fast
        self._limit = args.limit
        self._report_file = args.report_file
        self._resume_mode = args.resume
        self._selected = args.only
        self._target_dir = args.target_dir

        self._report = DownloadReport()

        self._matched_excluded: set[AnyId] = set()
        self._matched_selected: set[AnyId] = set()

        self._create_directories()

        if self._excluded:
            logger.debug("Will skip processing those resources: %s", format_csv_values(self._excluded))
        if self._selected:
            logger.debug("Will process only those resources: %s", format_csv_values(self._selected))

    def process_group(self, group: ResourceGroup) -> None:
        group_id = group.group_id

        self._report.register_group_start(group_id)

        # Check duplicate before filtering by CLI options to ensure the error is shown to the user,
        # even if the group is skipped.
        if self._report.is_group_already_processed(group_id):
            logger.error("Skipping duplicate resource group %r", group_id)
            self._report.register_group_failure(group_id, error=DuplicateResourceGroup(group_id))
            return

        skip_message = self._is_group_skipped_by_options(group_id)
        if skip_message is not None:
            self._report.register_group_skip(group_id, message=skip_message)
            return

        logger.debug("Starting to process resource group %r...", group_id)

        with Timer() as timer:
            try:
                group._start(downloader=self)  # noqa: SLF001
            except Exception as exc:
                self._report.register_group_failure(group_id, error=exc, timer=timer)
                logger.error(  # noqa: TRY400
                    "Error processing resource group %r",
                    group_id,
                    duration=format_timer(timer),
                    exc_info=not self._fail_fast,
                )
                if self._fail_fast:
                    raise
                return

        self._finalize_group(group)
        self._report.register_group_success(group_id, timer=timer)
        logger.info("Resource group %r has been processed successfully", group_id, duration=format_timer(timer))

    @overload
    def process_resource(
        self,
        resource: Resource[T],
        *,
        required: Literal[False] = False,
        serializer: "Serializer[T] | None" = None,
        source: Source,
    ) -> T | None:
        ...

    @overload
    def process_resource(
        self,
        resource: Resource[T],
        *,
        required: Literal[True],
        serializer: "Serializer[T] | None" = None,
        source: Source,
    ) -> T:
        ...

    @overload
    def process_resource(
        self,
        resource: Resource[T],
        *,
        required: bool = False,
        serializer: "Serializer[T] | None" = None,
        source: Source,
    ) -> T | None:
        ...

    # TODO do not skip required resources
    # context:
    # dbnomics_fetcher_toolbox.errors.downloader.ResourceSkipped: Resource 'catalogue-json' was skipped
    # 2023-11-29 17:16:44,476 [290597] WARNING  dbnomics_fetcher_toolbox.downloader: Some items of --only CLI option have not matched any resource or group: dataset-CFT

    def process_resource(
        self,
        resource: Resource[T],
        *,
        required: bool = False,
        serializer: "Serializer[T] | None" = None,
        source: Source,
    ) -> T | None:
        loaded_value = self._process_resource(resource, required=required, serializer=serializer, source=source)
        if required:
            return loaded_value.unwrap()
        return loaded_value.value_or(None)

    def start(self) -> None:
        with Timer() as timer:
            try:
                self._process()
            except Exception:
                logger.error(  # noqa: TRY400
                    "Error while running %r",
                    self._process.__qualname__,
                    duration=format_timer(timer),
                    exc_info=not self._fail_fast,
                )
                if self._fail_fast:
                    raise
            finally:
                self._log_unmatched_filters()
                self._save_report()
                self._log_stats()

    def _create_directories(self) -> None:
        create_directory(self._cache_dir, kind="cache")
        create_directory(self._debug_dir, kind="debug")
        create_directory(self._target_dir, kind="target")

    def _finalize_group(self, group: "ResourceGroup") -> None:
        if not group._kept_resources:  # noqa: SLF001
            return

        target_files = []
        for resource in group._kept_resources:  # noqa: SLF001
            file = resource.file
            resource_full_id = ResourceFullId.from_group_and_resource(group, resource)
            cache_file = self._cache_dir / file
            target_file = self._target_dir / file
            if self._resume_mode and target_file.is_file():
                logger.debug(
                    "Ignoring file %r of resource %r because it is already in target dir %r",
                    str(file),
                    str(resource_full_id),
                    str(self._target_dir),
                )
                continue
            if not cache_file.is_file():
                logger.error(
                    "Ignoring file %r of resource %r because it does not exist in cache dir %r",
                    str(file),
                    str(resource_full_id),
                    str(self._cache_dir),
                )
                continue

            move_file(cache_file, target_file)
            target_files.append(target_file)

        logger.debug(
            "Moved files of resources of group %r from cache dir to target dir: %s",
            group.group_id,
            format_csv_values(map(format_file_path_with_size, target_files)),
        )

    def _is_group_skipped_by_options(self, group_id: ResourceGroupId) -> str | None:
        if self._excluded is not None and group_id in self._excluded:
            self._matched_excluded.add(group_id)
            return f"Skipping group {group_id!r} because it is mentioned by --exclude CLI option"

        if self._selected is not None:
            if group_id in self._selected:
                self._matched_selected.add(group_id)
            else:
                return f"Skipping group {group_id!r} because it is not mentioned by --only CLI option"

        return None

    def _is_resource_skipped_by_options(self, resource_full_id: ResourceFullId) -> str | None:
        resource_group_id = resource_full_id.group_id

        if self._excluded is not None:
            if str(resource_full_id) in self._excluded:
                self._matched_excluded.add(resource_full_id)
                return f"Skipping resource {str(resource_full_id)!r} because it is mentioned by --exclude CLI option"

            if resource_group_id in self._excluded:
                self._matched_excluded.add(resource_full_id)
                return f"Skipping resource {str(resource_full_id)!r} because its group {resource_group_id} is mentioned by --exclude CLI option"  # noqa: E501

        if self._selected is not None:
            if str(resource_full_id) in self._selected or resource_group_id in self._selected:
                self._matched_selected.add(resource_full_id)
            else:
                return f"Skipping resource {str(resource_full_id)!r} because it is not mentioned by --only CLI option"

        if self._limit is not None and len(self._report.resource_full_ids) == self._limit:
            return (
                f"Skipping resource {str(resource_full_id)!r} because the limit provided by CLI option has been reached"
            )

        return None

    def _load_resource(
        self,
        resource: Resource[T],
        *,
        group: "ResourceGroup | None",
        keep: bool,
        resource_full_id: ResourceFullId,
        serializer: "Serializer[T] | None",
        source: Source,
        timer: Timer,
    ) -> T:
        file = resource.file
        cache_file = self._cache_dir / file
        target_file = self._target_dir / file

        # Ensure that file's parent directory exists, in case file contains a sub-directory.
        cache_file.parent.mkdir(exist_ok=True, parents=True)

        output_file: Path

        if self._resume_mode and target_file.is_file():
            output_file = target_file
            resume_message = f"Resume mode: reloading existing file of resource {str(resource_full_id)!r} from target dir: {format_file_path_with_size(target_file)}"  # noqa: E501
            logger.debug(resume_message)
            loaded_value = resource.parser.parse_file(target_file)
            self._report.register_resource_skip(resource_full_id, message=resume_message, timer=timer)
        else:
            output_file = cache_file

            if self._resume_mode and cache_file.is_file():
                resume_message = f"Resume mode: reloading existing file of resource {str(resource_full_id)!r} from cache dir: {format_file_path_with_size(cache_file)}"  # noqa: E501
                logger.debug(resume_message)
                loaded_value = resource.parser.parse_file(cache_file)
            else:
                logger.debug("Loading resource content from source %r...", type(source).__qualname__)
                with Timer() as timer:
                    loaded_value = source.load(
                        debug_dir=self._debug_dir,
                        output_file=cache_file,
                        parser=resource.parser,
                        resource_full_id=resource_full_id,
                        serializer=serializer,
                    )
                logger.debug(
                    "Loaded resource content from source successfully to %s",
                    format_file_path_with_size(cache_file),
                    duration=format_timer(timer),
                )

            if keep:
                if group:
                    group._kept_resources.append(resource)  # noqa: SLF001
                else:
                    move_file(cache_file, target_file)
                    logger.debug(
                        "Moved file of resource %r from cache dir to target dir because keep=True: %s",
                        str(resource_full_id),
                        format_file_path_with_size(target_file),
                    )
                    output_file = target_file

            self._report.register_resource_success(resource_full_id, output_file=output_file, timer=timer)
            logger.info(
                "Resource %r has been processed successfully and written to %s",
                str(resource_full_id),
                format_file_path_with_size(output_file),
                duration=format_timer(timer),
            )

        return loaded_value

    def _log_stats(self) -> None:
        logger.info(self._report.build_stats())

    def _log_unmatched_filters(self) -> None:
        def as_str(values: set[AnyId]) -> set[str]:
            return {str(value) for value in values}

        if self._excluded is not None and (
            unmatched_excluded := as_str(set(self._excluded)) - as_str(self._matched_excluded)
        ):
            logger.warning(
                "Some items of --exclude CLI option have not matched any resource or group: %s",
                format_csv_values(unmatched_excluded),
            )

        if self._selected is not None and (
            unmatched_selected := as_str(set(self._selected)) - as_str(self._matched_selected)
        ):
            logger.warning(
                "Some items of --only CLI option have not matched any resource or group: %s",
                format_csv_values(unmatched_selected),
            )

    @abstractmethod
    def _process(self) -> None:
        ...

    def _process_group_resource(
        self,
        resource: Resource[T],
        *,
        group: "ResourceGroup",
        keep: bool,
        required: bool,
        serializer: "Serializer[T] | None",
        source: Source,
    ) -> Maybe[T]:
        try:
            return self._process_resource(
                resource, group=group, keep=keep, required=required, serializer=serializer, source=source
            )
        except ResourceSkipped as exc:
            raise GroupAbortedAfterResourceSkipped(group=group, resource=resource) from exc

    def _process_resource(
        self,
        resource: Resource[T],
        *,
        group: "ResourceGroup | None" = None,
        keep: bool = True,
        required: bool,
        serializer: "Serializer[T] | None",
        source: Source,
    ) -> Maybe[T]:
        resource_full_id = ResourceFullId.from_group_and_resource(group, resource)

        self._report.register_resource_start(resource_full_id)

        # Check duplicate before filtering by CLI options to ensure the error is shown to the user,
        # even if the resource is skipped.
        if self._report.is_resource_already_processed(resource_full_id):
            logger.error("Skipping duplicate resource %r", str(resource_full_id))
            error = DuplicateResource(resource_full_id)
            self._report.register_resource_failure(resource_full_id, error=error)
            if not required:
                return Nothing
            raise ResourceSkipped(group=group, resource=resource) from error

        skip_message = self._is_resource_skipped_by_options(resource_full_id)
        if skip_message is not None:
            if required:
                logger.debug("Don't skip resource %r because it is required", str(resource_full_id))
            else:
                self._report.register_resource_skip(resource_full_id, message=skip_message)
                return Nothing

        logger.debug("Starting to process resource %r...", str(resource_full_id))

        with Timer() as timer:
            try:
                loaded_value = self._load_resource(
                    resource,
                    group=group,
                    keep=keep,
                    resource_full_id=resource_full_id,
                    serializer=serializer,
                    source=source,
                    timer=timer,
                )
            except Exception as exc:
                logger.log(
                    logging.ERROR if required else logging.WARNING,
                    "Error processing resource %r",
                    str(resource_full_id),
                    duration=format_timer(timer),
                    exc_info=not self._fail_fast,
                )
                if required:
                    self._report.register_resource_failure(resource_full_id, error=exc, timer=timer)
                if self._fail_fast:
                    raise
                if not required:
                    return Nothing
                raise ResourceLoadError(group=group, resource=resource) from exc

        return Some(loaded_value)

    def _save_report(self) -> None:
        if self._report_file is None:
            logger.debug("Skip saving the download report because no report file has been given")
            return

        self._report_file.write_bytes(self._report.dump_as_json_bytes())
        logger.info("Download report saved to %s", format_file_path_with_size(self._report_file))

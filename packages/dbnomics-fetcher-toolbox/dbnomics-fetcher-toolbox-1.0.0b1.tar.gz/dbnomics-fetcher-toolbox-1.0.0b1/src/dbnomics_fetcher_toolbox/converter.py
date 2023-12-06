from abc import ABC, abstractmethod
from pathlib import Path
from typing import TypeVar

import daiquiri
from contexttimer import Timer
from dbnomics_data_model.model import DatasetCode, DatasetId, ProviderCode
from dbnomics_data_model.storage import open_storage_from_uri_or_dir, open_storage_session_from_uri_or_dir

from dbnomics_fetcher_toolbox._internal.file_utils import create_directory, format_file_path_with_size
from dbnomics_fetcher_toolbox._internal.formatting_utils import format_csv_values, format_timer
from dbnomics_fetcher_toolbox._internal.reports.convert_report import ConvertReport
from dbnomics_fetcher_toolbox.convert_cli import ConvertCLIArgs
from dbnomics_fetcher_toolbox.dataset_converter import DatasetConverter
from dbnomics_fetcher_toolbox.errors.converter import DuplicateDataset
from dbnomics_fetcher_toolbox.resource import Resource

__all__ = ["Converter"]


logger = daiquiri.getLogger(__name__)


T = TypeVar("T")


class Converter(ABC):
    def __init__(self, *, args: ConvertCLIArgs, provider_code: ProviderCode | str) -> None:
        self._excluded = args.exclude
        self._fail_fast = args.fail_fast
        self._limit = args.limit
        self._report_file = args.report_file
        self._resume_mode = args.resume
        self._selected = args.only
        self._source_dir = args.source_dir
        self._target_storage_uri_or_dir = args.target_storage_uri_or_dir

        provider_code = ProviderCode.parse(provider_code)
        self.provider_code = provider_code

        self._report = ConvertReport()

        self._matched_excluded: set[DatasetCode] = set()
        self._matched_selected: set[DatasetCode] = set()

        self._create_directories()

        self.storage = open_storage_from_uri_or_dir(self._target_storage_uri_or_dir, ensure_dir=True)

        if self._excluded:
            logger.debug("Will skip processing those datasets: %s", format_csv_values(self._excluded))
        if self._selected:
            logger.debug("Will process only those datasets: %s", format_csv_values(self._selected))

    def load_resource(self, resource: Resource[T]) -> T:
        input_file = self._source_dir / resource.file
        return resource.parser.parse_file(input_file)

    def process_dataset(self, dataset_converter: DatasetConverter) -> None:
        dataset_code = dataset_converter.dataset_code
        dataset_id = dataset_converter.dataset_id

        self._report.register_dataset_start(dataset_code)

        # Check duplicate before filtering by CLI options to ensure the error is shown to the user,
        # even if the dataset is skipped.
        if self._report.is_dataset_already_processed(dataset_code):
            logger.error("Skipping duplicate dataset %r", str(dataset_code))
            self._report.register_dataset_failure(dataset_code, error=DuplicateDataset(dataset_code))
            return

        skip_message = self._is_dataset_skipped_by_options(dataset_code)
        if skip_message is not None:
            self._report.register_dataset_skip(dataset_code, message=skip_message)
            return

        if self._resume_mode and self.storage.has_dataset(dataset_id):
            skip_message = f"Resume mode: skipping dataset {str(dataset_code)!r} because it already exists in storage"
            logger.debug(skip_message, dataset_code=str(dataset_code))
            self._report.register_dataset_skip(dataset_code, message=skip_message)
            return

        logger.debug("Starting to process dataset %r...", str(dataset_code))

        self._delete_dataset_if_exists(dataset_id)

        with open_storage_session_from_uri_or_dir(
            self._target_storage_uri_or_dir, ensure_dir=True
        ) as session, Timer() as timer:
            try:
                dataset_converter._start(converter=self, session=session)  # noqa: SLF001
            except Exception as exc:
                self._report.register_dataset_failure(dataset_code, error=exc, timer=timer)
                logger.error(  # noqa: TRY400
                    "Error processing dataset %r",
                    str(dataset_code),
                    duration=format_timer(timer),
                    exc_info=not self._fail_fast,
                )
                if self._fail_fast:
                    raise
                return

            session.commit()
            self._report.register_dataset_success(dataset_code, timer=timer)
            logger.info("Dataset %r has been processed successfully", str(dataset_id), duration=format_timer(timer))

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

        self._log_unmatched_filters()
        self._save_report()
        self._log_stats()

    def _create_directories(self) -> None:
        if isinstance(self._target_storage_uri_or_dir, Path):
            create_directory(self._target_storage_uri_or_dir, kind="target")

    def _delete_dataset_if_exists(self, dataset_id: DatasetId) -> None:
        if not self.storage.has_dataset(dataset_id):
            return

        self.storage.delete_dataset(dataset_id)
        logger.debug("Deleted already existing dataset %r", str(dataset_id))

    def _is_dataset_skipped_by_options(self, dataset_code: DatasetCode) -> str | None:
        if self._excluded is not None and dataset_code in self._excluded:
            self._matched_excluded.add(dataset_code)
            return f"Skipping dataset {str(dataset_code)!r} because it is mentioned by --exclude CLI option"

        if self._selected is not None:
            if dataset_code in self._selected:
                self._matched_selected.add(dataset_code)
            else:
                return f"Skipping dataset {str(dataset_code)!r} because it is not mentioned by --only CLI option"

        if self._limit is not None and len(self._report.dataset_codes) == self._limit:
            return f"Skipping dataset {str(dataset_code)!r} because the limit provided by CLI option has been reached"

        return None

    def _log_stats(self) -> None:
        logger.info(self._report.build_stats())

    def _log_unmatched_filters(self) -> None:
        if self._excluded is not None and (unmatched_excluded := set(self._excluded) - self._matched_excluded):
            logger.warning(
                "Some items of --exclude CLI option have not matched any dataset: %s",
                format_csv_values(unmatched_excluded),
            )
        if self._selected is not None and (unmatched_selected := set(self._selected) - self._matched_selected):
            logger.warning(
                "Some items of --only CLI option have not matched any dataset: %s",
                format_csv_values(unmatched_selected),
            )

    @abstractmethod
    def _process(self) -> None:
        ...

    def _save_report(self) -> None:
        if self._report_file is None:
            logger.debug("Skip saving the convert report because no report file has been given")
            return

        self._report_file.write_bytes(self._report.dump_as_json_bytes())
        logger.info("Convert report has been saved to %s", format_file_path_with_size(self._report_file))

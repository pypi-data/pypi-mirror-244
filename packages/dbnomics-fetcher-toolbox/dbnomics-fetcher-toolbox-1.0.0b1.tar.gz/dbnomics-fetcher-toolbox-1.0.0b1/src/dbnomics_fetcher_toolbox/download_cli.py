import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Self, cast

import daiquiri

from ._internal.argparse_utils import AnyId, csv_any_ids, positive
from ._internal.base_cli import (
    EXCLUDE_OPTION_NAME,
    LIMIT_OPTION_NAME,
    ONLY_OPTION_NAME,
    BaseCLIArgs,
    BaseCLIArgsParser,
)

__all__ = ["DownloadCLIArgs", "DownloadCLIArgsParser"]

logger = daiquiri.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class DownloadCLIArgs(BaseCLIArgs):
    cache_dir: Path | None
    debug_dir: Path | None
    exclude: list[AnyId]
    limit: int | None
    only: list[AnyId]
    report_file: Path | None
    target_dir: Path

    @classmethod
    def parse(cls) -> Self:
        parser = DownloadCLIArgsParser(args_class=cls)
        args_namespace = parser.parse_args_namespace()
        return cast(Self, args_namespace)


class DownloadCLIArgsParser(BaseCLIArgsParser):
    def setup_argparse_parser(self, argparse_parser: argparse.ArgumentParser) -> None:
        super().setup_argparse_parser(argparse_parser)

        argparse_parser.add_argument("target_dir", type=Path, help="directory where provider data is written to")

        argparse_parser.add_argument(
            "--cache-dir",
            default=self.env("TOOLBOX_CACHE_DIR", None),
            help="directory where non-kept files can be written to (e.g. ZIP files)",
            type=Path,
        )
        argparse_parser.add_argument(
            "--debug-dir",
            default=self.env("TOOLBOX_DEBUG_DIR", None),
            help="directory where debug files can be written to (e.g. failed HTTP responses)",
            type=Path,
        )
        argparse_parser.add_argument(
            LIMIT_OPTION_NAME,
            default=self.env("TOOLBOX_DOWNLOAD_RESOURCE_LIMIT", None),
            help="download a maximum number of resources",
            type=positive(int),
        )
        argparse_parser.add_argument(
            "--report-file",
            default=self.env("TOOLBOX_DOWNLOAD_REPORT_FILE", "download_report.json"),
            help="output file to write the error report to",
            type=Path,
        )

        resource_selection = argparse_parser.add_mutually_exclusive_group()
        resource_selection.add_argument(
            EXCLUDE_OPTION_NAME,
            default=self.env("TOOLBOX_EXCLUDE_RESOURCES", None),
            help="do not download the specified resources",
            type=csv_any_ids,
        )
        resource_selection.add_argument(
            ONLY_OPTION_NAME,
            default=self.env("TOOLBOX_ONLY_RESOURCES", None),
            help="download only the specified resources",
            type=csv_any_ids,
        )

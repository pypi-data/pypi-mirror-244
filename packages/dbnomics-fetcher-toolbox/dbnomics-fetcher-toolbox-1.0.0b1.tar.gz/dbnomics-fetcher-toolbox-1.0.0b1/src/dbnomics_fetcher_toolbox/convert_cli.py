import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Self, cast

import daiquiri
from dbnomics_data_model.model import DatasetCode
from dbnomics_data_model.storage import StorageUri, parse_storage_uri_or_dir
from dbnomics_data_model.storage.errors.storage_uri import StorageUriParseError

from dbnomics_fetcher_toolbox._internal.argparse_utils import csv_dataset_codes, positive

from ._internal.base_cli import EXCLUDE_OPTION_NAME, LIMIT_OPTION_NAME, ONLY_OPTION_NAME, BaseCLIArgs, BaseCLIArgsParser

__all__ = ["ConvertCLIArgs", "ConvertCLIArgsParser"]


logger = daiquiri.getLogger(__package__)


@dataclass(frozen=True, kw_only=True)
class ConvertCLIArgs(BaseCLIArgs):
    exclude: list[DatasetCode]
    limit: int | None
    only: list[DatasetCode]
    report_file: Path | None
    source_dir: Path
    target_storage_uri_or_dir: StorageUri | Path

    @classmethod
    def parse(cls) -> Self:
        parser = ConvertCLIArgsParser(args_class=cls)
        args_namespace = parser.parse_args_namespace()
        try:
            args_namespace.target_storage_uri_or_dir = parse_storage_uri_or_dir(
                args_namespace.target_storage_uri_or_dir
            )
        except StorageUriParseError as exc:
            parser.fail(msg=str(exc))

        return cast(Self, args_namespace)


class ConvertCLIArgsParser(BaseCLIArgsParser):
    def setup_argparse_parser(self, argparse_parser: argparse.ArgumentParser) -> None:
        super().setup_argparse_parser(argparse_parser)

        argparse_parser.add_argument("source_dir", type=Path, help="directory where provider data is read from")
        argparse_parser.add_argument(
            "target_storage_uri_or_dir",
            default=self.env("TOOLBOX_TARGET_STORAGE_URI_OR_DIR", None),
            help="URI of the storage adapter used to write converted data, or a directory",
            type=str,
        )

        argparse_parser.add_argument(
            LIMIT_OPTION_NAME,
            default=self.env("TOOLBOX_CONVERT_DATASET_LIMIT", None),
            help="build a maximum number of datasets",
            type=positive(int),
        )
        argparse_parser.add_argument(
            "--report-file",
            default=self.env("TOOLBOX_CONVERT_REPORT_FILE", "convert_report.json"),
            help="output file to write the error report to",
            type=Path,
        )

        dataset_selection = argparse_parser.add_mutually_exclusive_group()
        dataset_selection.add_argument(
            EXCLUDE_OPTION_NAME,
            default=self.env("TOOLBOX_EXCLUDE_DATASETS", None),
            help="do not convert the specified datasets",
            type=csv_dataset_codes,
        )
        dataset_selection.add_argument(
            ONLY_OPTION_NAME,
            default=self.env("TOOLBOX_ONLY_DATASETS", None),
            help="convert only the specified datasets",
            type=csv_dataset_codes,
        )

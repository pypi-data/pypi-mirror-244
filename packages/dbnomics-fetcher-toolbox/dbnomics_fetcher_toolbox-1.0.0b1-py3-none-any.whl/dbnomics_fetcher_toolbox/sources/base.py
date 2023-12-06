from abc import ABC, abstractmethod
from collections.abc import Iterator
from pathlib import Path
from typing import TYPE_CHECKING, TypeVar

import daiquiri

from dbnomics_fetcher_toolbox._internal.file_utils import write_chunks

if TYPE_CHECKING:
    from dbnomics_fetcher_toolbox.parsers.base import FileParser
    from dbnomics_fetcher_toolbox.serializers.base import Serializer
    from dbnomics_fetcher_toolbox.types import ResourceFullId


__all__ = ["Source"]

logger = daiquiri.getLogger(__name__)


T = TypeVar("T")


class Source(ABC):
    @abstractmethod
    def iter_bytes(self, *, debug_dir: Path | None, resource_full_id: "ResourceFullId") -> Iterator[bytes]:
        ...

    def load(
        self,
        *,
        debug_dir: Path | None,
        output_file: Path,
        parser: "FileParser[T]",
        resource_full_id: "ResourceFullId",
        serializer: "Serializer[T] | None",
    ) -> T:
        source_content = self.iter_bytes(debug_dir=debug_dir, resource_full_id=resource_full_id)

        if serializer is None:
            serializer = parser.default_serializer

        if serializer is None:
            write_chunks(source_content, output_file=output_file)
            return parser.parse_file(output_file)

        raw_output_file = output_file.with_suffix(f"{output_file.suffix}.raw")
        write_chunks(source_content, output_file=raw_output_file)

        parsed_value = parser.parse_file(raw_output_file)

        serialized_value = serializer.serialize(parsed_value)
        write_chunks(serialized_value, output_file=output_file)

        raw_output_file.unlink()

        return parsed_value

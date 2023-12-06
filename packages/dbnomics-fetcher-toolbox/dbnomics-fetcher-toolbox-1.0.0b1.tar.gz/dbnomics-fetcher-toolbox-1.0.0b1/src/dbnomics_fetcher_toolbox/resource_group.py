from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Literal, TypeVar, overload

import daiquiri

from dbnomics_fetcher_toolbox.resource import Resource
from dbnomics_fetcher_toolbox.types import ResourceGroupId

if TYPE_CHECKING:
    from dbnomics_fetcher_toolbox.downloader import Downloader
    from dbnomics_fetcher_toolbox.serializers.base import Serializer
    from dbnomics_fetcher_toolbox.sources.base import Source

__all__ = ["ResourceGroup"]


logger = daiquiri.getLogger(__name__)


T = TypeVar("T")


class ResourceGroup(ABC):
    def __init__(self, *, group_id: "ResourceGroupId | str") -> None:
        group_id = ResourceGroupId.parse(group_id)
        self.group_id = group_id

    def __repr__(self) -> str:
        return f"{type(self).__name__}(id={self.group_id!r})"

    @overload
    def process_resource(
        self,
        resource: Resource[T],
        *,
        keep: bool = True,
        required: Literal[True] = True,
        serializer: "Serializer[T] | None" = None,
        source: "Source",
    ) -> T:
        ...

    @overload
    def process_resource(
        self,
        resource: Resource[T],
        *,
        keep: bool = True,
        required: Literal[False],
        serializer: "Serializer[T] | None" = None,
        source: "Source",
    ) -> T | None:
        ...

    @overload
    def process_resource(
        self,
        resource: Resource[T],
        *,
        keep: bool = True,
        required: bool = True,
        serializer: "Serializer[T] | None" = None,
        source: "Source",
    ) -> T | None:
        ...

    def process_resource(
        self,
        resource: Resource[T],
        *,
        keep: bool = True,
        required: bool = True,
        serializer: "Serializer[T] | None" = None,
        source: "Source",
    ) -> T | None:
        loaded_value = self._downloader._process_group_resource(  # noqa: SLF001
            resource, group=self, keep=keep, required=required, serializer=serializer, source=source
        )
        if required:
            return loaded_value.unwrap()
        return loaded_value.value_or(None)

    @abstractmethod
    def _process(self) -> None:
        ...

    def _start(self, *, downloader: "Downloader") -> None:
        self._downloader = downloader
        self._kept_resources: list[Resource[Any]] = []
        self._process()

from collections.abc import Callable
from typing import TYPE_CHECKING, Protocol, Self, TypeAlias

if TYPE_CHECKING:
    from dbnomics_fetcher_toolbox.bisect.model import BisectDimension


__all__ = ["PartitionId"]


PartitionId: TypeAlias = str


class BisectionPartition(Protocol):
    def bisect(self) -> tuple[Self, Self]:
        ...

    @property
    def partition_id(self) -> PartitionId:
        ...


BisectDimensionCode: TypeAlias = str
BisectDimensionValueCode: TypeAlias = str
SeriesMask: TypeAlias = str


DimensionSelector: TypeAlias = Callable[[list["BisectDimension"]], BisectDimensionCode]
PartitionIdBuilder: TypeAlias = Callable[[list["BisectDimension"]], PartitionId]

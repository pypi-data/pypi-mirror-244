from dataclasses import dataclass
from typing import Generic, TypeVar

from dbnomics_fetcher_toolbox.bisect.types import BisectionPartition

TBisectionPartition = TypeVar("TBisectionPartition", bound=BisectionPartition)


@dataclass(frozen=True, kw_only=True)
class PartitionAttempt(Generic[TBisectionPartition]):
    depth: int
    partition: TBisectionPartition
    # partition_id: PartitionId
    # dimensions: list[BisectDimension]
    # series_mask: SeriesMask

from typing import TYPE_CHECKING

from dbnomics_fetcher_toolbox.bisect.types import BisectDimensionCode
from dbnomics_fetcher_toolbox.errors.base import FetcherToolboxError

if TYPE_CHECKING:
    from dbnomics_fetcher_toolbox.bisect.model import BisectDimension


class BisectError(FetcherToolboxError):
    pass


class BisectDimensionNotFound(BisectError):
    def __init__(self, code: BisectDimensionCode, *, dimensions: list["BisectDimension"]) -> None:
        msg = f"Dimension {code!r} not found"
        super().__init__(msg=msg)
        self.code = code
        self.dimensions = dimensions


class NoBisectDimension(BisectError):
    def __init__(self) -> None:
        msg = "Can't bisect an empty dimension list"
        super().__init__(msg=msg)


class NoBisectableDimension(BisectError):
    def __init__(self, *, dimensions: list["BisectDimension"]) -> None:
        msg = "All dimensions have one value, can't bisect"
        super().__init__(msg=msg)
        self.dimensions = dimensions

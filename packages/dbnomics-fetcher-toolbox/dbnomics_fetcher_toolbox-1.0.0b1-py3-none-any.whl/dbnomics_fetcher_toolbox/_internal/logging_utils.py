"""Logging utility functions."""


from collections.abc import Iterable
from typing import Final

import daiquiri
from daiquiri.formatter import ColorExtrasFormatter
from daiquiri.output import Stream

DEFAULT_FORMAT: Final = (
    "%(asctime)s [%(process)d] %(color)s%(levelname)-8.8s %(name)s: %(message)s%(extras)s%(color_stop)s"
)

# TODO use dictConfig? or other library like structlog?


def setup_logging(*, log_format: str | None = None, log_levels: Iterable[str]) -> None:
    """Setup logging using the provided log format and log level.

    This only sets the level of the loggers of the dbnomics_fetcher_toolbox package, and current Python script.
    This does not modify the level of the third-party packages (e.g. requests, urllib3, etc.).
    """  # noqa: D401
    if log_format is None:
        log_format = DEFAULT_FORMAT

    daiquiri.setup(
        outputs=[
            Stream(formatter=ColorExtrasFormatter(fmt=log_format)),
        ],
    )
    daiquiri.parse_and_set_default_log_levels(log_levels)

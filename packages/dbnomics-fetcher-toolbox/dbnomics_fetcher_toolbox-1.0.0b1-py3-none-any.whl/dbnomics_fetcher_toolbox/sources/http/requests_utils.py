from datetime import timedelta
from pathlib import Path
from typing import TYPE_CHECKING, Final

import daiquiri
import requests
import requests_toolbelt.utils.dump
from humanfriendly import format_timespan
from requests import Response, Session
from requests.exceptions import ChunkedEncodingError, HTTPError, RequestException, Timeout
from tenacity import (
    Retrying,
    retry_if_exception,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from dbnomics_fetcher_toolbox._internal.file_utils import format_file_path_with_size

if TYPE_CHECKING:
    from requests.api import _HeadersMapping
    from requests.sessions import _Params, _Timeout
    from tenacity import RetryCallState


__all__ = [
    "default_retrying_retry",
    "default_retrying_stop",
    "default_retrying_wait",
    "default_retrying",
    "retry_if_bad_http_status_code",
]


logger = daiquiri.getLogger(__name__)


def fetch_url(
    url: str,
    *,
    headers: "_HeadersMapping | None" = None,
    method: str | None = None,
    params: "_Params | None" = None,
    response_dump_file: Path | None = None,
    session: Session | None = None,
    stream: bool = True,
    timeout: "_Timeout",
) -> Response:
    if method is None:
        method = "get"

    request_func = requests.request if session is None else session.request

    response = request_func(method, url, headers=headers, params=params, stream=stream, timeout=timeout)

    try:
        response.raise_for_status()
    except RequestException:
        if response_dump_file is not None:
            save_http_response_dump(response, output_file=response_dump_file)
        raise

    if response_dump_file is not None:
        save_http_response_dump(response, output_file=response_dump_file)

    return response


def save_http_response_dump(response: Response, *, output_file: Path) -> None:
    response_dump = requests_toolbelt.utils.dump.dump_all(response)
    output_file.write_bytes(response_dump)
    logger.debug("Saved response dump to debug directory: %s", format_file_path_with_size(output_file))


def log_before_attempt(retry_state: "RetryCallState") -> None:
    logger.debug("Loading source, attempt %d", retry_state.attempt_number)


def log_before_sleep(retry_state: "RetryCallState") -> None:
    assert retry_state.next_action is not None
    sleep_duration = retry_state.next_action.sleep
    logger.debug("Sleeping %s", format_timespan(sleep_duration))


def log_failed_attempt(retry_state: "RetryCallState") -> None:
    outcome = retry_state.outcome
    assert outcome is not None

    msg = "Error loading source"

    duration = retry_state.seconds_since_start
    if duration is not None:
        msg += f" after {format_timespan(duration)}"

    msg += f", attempt {retry_state.attempt_number}"

    try:
        outcome.result()
    except Exception:
        logger.exception(msg)
    else:
        logger.error(msg)


def should_retry_http_status_code(exception: BaseException) -> bool:
    http_codes_to_retry = [408, 425, 429, 500, 502, 503, 504]

    if isinstance(exception, HTTPError):
        status_code = exception.response.status_code  # type:ignore[union-attr]
        return status_code in http_codes_to_retry

    return False


retry_if_bad_http_status_code = retry_if_exception(predicate=should_retry_http_status_code)

default_retrying_retry: Final = retry_if_bad_http_status_code | retry_if_exception_type((ChunkedEncodingError, Timeout))
default_retrying_stop: Final = stop_after_attempt(5)
# TODO here we wait max(2**0,5)=5, max(2**1,5)=5, max(2**2,5)=5, max(2**3,5)=8, could we have better 5, 10, 20, ...?
default_retrying_wait: Final = wait_exponential(max=timedelta(minutes=15), min=timedelta(seconds=5), multiplier=1)
default_retrying: Final = Retrying(
    after=log_failed_attempt,
    before=log_before_attempt,
    # TODO perfect the logging message (remove exception message, and URL)
    before_sleep=log_before_sleep,
    retry=default_retrying_retry,
    stop=default_retrying_stop,
    wait=default_retrying_wait,
)

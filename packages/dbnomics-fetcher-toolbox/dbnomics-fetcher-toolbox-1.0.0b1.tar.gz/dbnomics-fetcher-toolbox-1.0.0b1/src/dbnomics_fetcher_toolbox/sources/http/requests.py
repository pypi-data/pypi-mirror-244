import codecs
from collections.abc import Iterator
from datetime import timedelta
from pathlib import Path
from typing import TYPE_CHECKING, Final, Literal, TypeVar

import daiquiri
from humanfriendly import format_timespan
from requests import Session

from dbnomics_fetcher_toolbox.parsers.base import FileParser
from dbnomics_fetcher_toolbox.sources.base import Source
from dbnomics_fetcher_toolbox.sources.http.requests_utils import default_retrying, fetch_url

if TYPE_CHECKING:
    from requests.api import _HeadersMapping
    from requests.sessions import _Params
    from tenacity import BaseRetrying

    from dbnomics_fetcher_toolbox.serializers.base import Serializer
    from dbnomics_fetcher_toolbox.types import ResourceFullId


__all__ = ["RequestsHttpSource"]


logger = daiquiri.getLogger(__name__)

T = TypeVar("T")


DEFAULT_TIMEOUT: Final = timedelta(minutes=1)
HTTP_DEBUG_DIR_NAME: Final = "http"


class RequestsHttpSource(Source):
    def __init__(
        self,
        *,
        chunk_size: int | None = None,
        connect_timeout: float | timedelta | None = None,
        decoder_errors: str | None = None,
        encoding: str | None = None,
        headers: "_HeadersMapping | None" = None,
        method: str | None = None,
        params: "_Params | None" = None,
        read_timeout: float | timedelta | None = None,
        retrying: "BaseRetrying | Literal[False] | None" = None,
        session: Session | None = None,
        stream: bool = True,
        url: str,
        use_response_charset: bool | str = True,
    ) -> None:
        def normalize_timeout(timeout: float | timedelta | None) -> float:
            if timeout is None:
                # Avoid doing a request without timeout, because it could take an infinite time if the server has no timeout.
                return DEFAULT_TIMEOUT.total_seconds()

            if isinstance(timeout, timedelta):
                return timeout.total_seconds()

            return timeout

        self.chunk_size = chunk_size
        self.connect_timeout = normalize_timeout(connect_timeout)

        if decoder_errors is None:
            decoder_errors = "strict"
        self.decoder_errors = decoder_errors

        if encoding is None:
            encoding = "utf-8"
        self.encoding = encoding

        self.headers = headers
        self.method = method
        self.params = params
        self.read_timeout = normalize_timeout(read_timeout)

        if retrying is None:
            retrying = default_retrying
        self._retrying = retrying

        self.stream = stream
        self.url = url
        self.use_response_charset = use_response_charset

        self._response_dump_file: Path | None = None
        self._session = session

    def iter_bytes(
        self, *, debug_dir: Path | None, resource_full_id: "ResourceFullId"  # noqa: ARG002
    ) -> Iterator[bytes]:
        logger.debug(
            "Fetching URL %r (connect timeout: %s, read timeout: %s)...",
            self.url,
            format_timespan(self.connect_timeout),
            format_timespan(self.read_timeout),
            resource_full_id=resource_full_id,
        )

        response = fetch_url(
            self.url,
            headers=self.headers,
            method=self.method,
            params=self.params,
            response_dump_file=self._response_dump_file,
            session=self._session,
            stream=self.stream,
            timeout=(self.connect_timeout, self.read_timeout),
        )

        logger.debug("Received HTTP response: %r", response)

        use_response_charset = self.use_response_charset
        content_iter = response.iter_content(chunk_size=self.chunk_size)
        if use_response_charset is True and response.encoding is not None:
            content_iter = self._reencode(content_iter, from_encoding=response.encoding)
        elif isinstance(use_response_charset, str):
            content_iter = self._reencode(content_iter, from_encoding=use_response_charset)
        return content_iter

    def load(
        self,
        *,
        debug_dir: Path | None,
        output_file: Path,
        parser: FileParser[T],
        resource_full_id: "ResourceFullId",
        serializer: "Serializer[T] | None",
    ) -> T:
        self._response_dump_file = None

        if self._retrying is False:
            return super().load(
                debug_dir=debug_dir,
                output_file=output_file,
                parser=parser,
                resource_full_id=resource_full_id,
                serializer=serializer,
            )

        for attempt in self._retrying:
            self._response_dump_file = self._get_response_dump_file(
                resource_full_id, attempt_number=attempt.retry_state.attempt_number, debug_dir=debug_dir
            )
            with attempt:
                loaded_value = super().load(
                    debug_dir=debug_dir,
                    output_file=output_file,
                    parser=parser,
                    resource_full_id=resource_full_id,
                    serializer=serializer,
                )
            outcome = attempt.retry_state.outcome
            assert outcome is not None
            if not outcome.failed:
                attempt.retry_state.set_result(loaded_value)

        return loaded_value

    def _ensure_http_debug_dir(self, *, debug_dir: Path) -> Path:
        http_debug_dir = debug_dir / HTTP_DEBUG_DIR_NAME
        http_debug_dir.mkdir(exist_ok=True)
        return http_debug_dir

    def _get_response_dump_file(
        self,
        resource_full_id: "ResourceFullId",
        *,
        attempt_number: int,
        debug_dir: Path | None,
    ) -> Path | None:
        if debug_dir is None:
            return None

        http_debug_dir = self._ensure_http_debug_dir(debug_dir=debug_dir)

        file_name = f"{resource_full_id}.attempt_{attempt_number}.txt"
        return http_debug_dir / file_name

    def _reencode(self, content_iter: Iterator[bytes], *, from_encoding: str) -> Iterator[bytes]:
        decoder = codecs.getincrementaldecoder(from_encoding)(errors=self.decoder_errors)

        for chunk in content_iter:
            decoded_chunk = decoder.decode(chunk)
            if decoded_chunk:
                yield decoded_chunk.encode(self.encoding)
        decoded_chunk = decoder.decode(b"", final=True)
        if decoded_chunk:
            yield decoded_chunk.encode(self.encoding)

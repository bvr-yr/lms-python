"""Application logging configuration and performance profiling utilities."""

import logging
import sys
import time
from collections.abc import Callable, Generator
from contextlib import contextmanager
from functools import wraps
from typing import Any

from lms_python.config import app_settings

LOG_FORMAT = (
    "%(asctime)s | %(relative_sec)7s | %(levelname)-7s | %(name)-28s | %(message)s"
)
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class RelativeTimeFormatter(logging.Formatter):
    """Custom formatter injecting elapsed process execution time into log records."""

    def format(self, record: logging.LogRecord) -> str:
        """Compute relative_sec and format the incoming log record.

        :param record: The active log record being processed.
        :type record: logging.LogRecord
        :return: Formatted log message string.
        :rtype: str
        """
        record.relative_sec = f"{record.relativeCreated / 1000:.3f}s"
        return super().format(record)


def setup_logging() -> None:
    """Configure the root logger with handlers and formatting."""
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(RelativeTimeFormatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT))

    logging.basicConfig(
        level=app_settings.lms_log_level,
        handlers=[handler],
        force=True,
    )


logger = logging.getLogger(__name__)


@contextmanager
def timer(
    description: str, target_logger: logging.Logger | None = None
) -> Generator[None]:
    """Context manager measuring and logging block execution duration.

    :param description: Contextual label prepended to the elapsed time log.
    :type description: str
    :param target_logger: Target logger instance; defaults to the module logger.
    :type target_logger: logging.Logger | None
    :return: Context manager yielding execution control back to the caller.
    :rtype: Generator[None]
    """
    log = target_logger or logger
    now = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - now
        log.debug("%s finished in %.4f seconds", description, elapsed)


def perf_logger(func: Callable[..., Any]) -> Callable[..., Any]:
    """Log execution duration and callable identity at DEBUG level.

    :param func: Target callable to benchmark and wrap.
    :type func: Callable[..., Any]
    :return: Wrapped callable preserving the original signature and return value.
    :rtype: Callable[..., Any]
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        now = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - now
        _name = getattr(func, "__name__", "<unknown_name>")
        _type = getattr(type(func), "__name__", "<unknown_type>")

        logging.getLogger(func.__module__).debug(
            "%s '%s' executed in %.4f seconds", _type, _name, elapsed
        )
        return result

    return wrapper

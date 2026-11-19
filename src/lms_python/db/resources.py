"""Resource loading utilities for packaged SQL files."""

import logging
from importlib.resources import files
from typing import LiteralString, cast

logger = logging.getLogger(__name__)


def load_sql_resource(package: str, filename: str) -> LiteralString:
    """Read and return the contents of a bundled SQL resource file.

    :param package: Dot-separated package path containing the resource.
    :type package: str
    :param filename: Name of the SQL file to load.
    :type filename: str
    :return: Raw SQL file contents.
    :rtype: LiteralString
    """
    content = files(package).joinpath(filename).read_text(encoding="utf-8")
    logger.info("loaded %s from %s", filename, package)
    return cast("LiteralString", content)

import logging
from importlib.resources import files
from typing import LiteralString, cast

logger = logging.getLogger(__name__)


def load_sql_resource(package: str, filename: str) -> LiteralString:
    content = files(package).joinpath(filename).read_text(encoding="utf-8")
    logger.info("loaded %s from %s", filename, package)
    return cast("LiteralString", content)

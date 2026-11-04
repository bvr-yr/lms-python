from importlib.resources import files
from typing import LiteralString, cast


def load_sql_resource(package: str, filename: str) -> LiteralString:
    content = files(package).joinpath(filename).read_text(encoding="utf-8")
    return cast("LiteralString", content)

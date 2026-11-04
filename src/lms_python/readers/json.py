import json
from pathlib import Path
from typing import Any

from lms_python.readers.base import BaseReader


class JSONReader(BaseReader):
    def _read(self, path: Path) -> Any:
        with path.open(encoding="utf-8") as file:
            return json.load(file)

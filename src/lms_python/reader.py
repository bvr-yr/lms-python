import json
from pathlib import Path
from typing import Any


class JSONReader:
    def read(self, file_path: str | Path) -> list[dict[str, Any]]:
        path = Path(file_path).resolve()

        if not path.is_file():
            error_message = f"Source file not found at: {path!r}"
            raise FileNotFoundError(error_message)

        with path.open(encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            error_message = (
                f"Expected top-level JSON array in {path.name!r}, "
                f"got {type(data).__name__}"
            )
            raise TypeError(error_message)

        return data

"""JSON-specific exporter implementation."""

import json
from collections.abc import Sequence
from pathlib import Path

from pydantic import BaseModel

from lms_python.exporters.base import BaseExporter


class JSONExporter(BaseExporter):
    """Exports validated model sequences as formatted JSON arrays."""

    def _write(self, data: Sequence[BaseModel], path: Path) -> None:
        payload = [item.model_dump() for item in data]
        with path.open("w", encoding="utf-8") as file:
            json.dump(payload, file, indent=4, default=str, ensure_ascii=False)

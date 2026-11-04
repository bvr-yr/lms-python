import json
from pathlib import Path

from lms_python.exporters.base import BaseExporter, ExportData


class JSONExporter(BaseExporter):
    def _write(self, data: ExportData, path: Path) -> None:
        payload = [item.model_dump() for item in data]
        with path.open("w", encoding="utf-8") as file:
            json.dump(payload, file, indent=4, default=str, ensure_ascii=False)

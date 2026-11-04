from abc import ABC, abstractmethod
from collections.abc import Sequence
from pathlib import Path

from pydantic import BaseModel

type ExportData = Sequence[BaseModel]


class BaseExporter(ABC):
    def export(self, data: ExportData, output_path: str | Path) -> None:
        path = Path(output_path).resolve()
        path.parent.mkdir(parents=True, exist_ok=True)

        self._write(data, path)

    @abstractmethod
    def _write(self, data: ExportData, path: Path) -> None: ...

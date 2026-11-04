from abc import ABC, abstractmethod
from collections.abc import Sequence
from pathlib import Path

from pydantic import BaseModel


class BaseExporter(ABC):
    def export(self, data: Sequence[BaseModel], output_path: str | Path) -> None:
        path = Path(output_path).resolve()
        path.parent.mkdir(parents=True, exist_ok=True)

        self._write(data, path)

    @abstractmethod
    def _write(self, data: Sequence[BaseModel], path: Path) -> None: ...

import logging
from abc import ABC, abstractmethod
from collections.abc import Sequence
from pathlib import Path

from pydantic import BaseModel

from lms_python.logger import perf_logger

logger = logging.getLogger(__name__)


class BaseExporter(ABC):
    @perf_logger
    def export(self, data: Sequence[BaseModel], output_path: str | Path) -> None:
        path = Path(output_path).resolve()
        path.parent.mkdir(parents=True, exist_ok=True)

        self._write(data, path)
        logger.info("exported %d records to %s", len(data), output_path)

    @abstractmethod
    def _write(self, data: Sequence[BaseModel], path: Path) -> None: ...

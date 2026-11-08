"""Abstract base exporter definition."""

import logging
from abc import ABC, abstractmethod
from collections.abc import Sequence
from pathlib import Path

from pydantic import BaseModel

from lms_python.logger import perf_logger

logger = logging.getLogger(__name__)


class BaseExporter(ABC):
    """Abstract base class handling serialization and file destination preparation."""

    @perf_logger
    def export(self, data: Sequence[BaseModel], output_path: str | Path) -> None:
        """Ensure destination directories exist and delegate payload writing.

        :param data: Sequence of validated Pydantic models to export.
        :type data: Sequence[BaseModel]
        :param output_path: Destination file path.
        :type output_path: str | Path
        """
        path = Path(output_path).resolve()
        path.parent.mkdir(parents=True, exist_ok=True)

        self._write(data, path)
        logger.info("exported %d records to %s", len(data), output_path)

    @abstractmethod
    def _write(self, data: Sequence[BaseModel], path: Path) -> None:
        """Serialize data and write the payload directly to disk.

        :param data: Sequence of validated Pydantic models to serialize.
        :type data: Sequence[BaseModel]
        :param path: Resolved destination path.
        :type path: Path
        """

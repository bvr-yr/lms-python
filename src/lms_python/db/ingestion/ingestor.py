"""Bulk data ingestion handling."""

from collections.abc import Iterable

from pydantic import BaseModel

from lms_python.db.ingestion.protocols import DataLoader
from lms_python.db.ingestion.spec import IngestionSpec
from lms_python.logger import perf_logger


class DataIngestor:
    """Maps validated Pydantic models to database rows for bulk loading."""

    def __init__(self, loader: DataLoader) -> None:
        """Initialize the ingestor.

        :param loader: Configured DataLoader instance.
        :type loader: DataLoader
        """
        self._loader = loader

    @perf_logger
    def insert[T: BaseModel](
        self,
        items: Iterable[T],
        spec: IngestionSpec[T],
    ) -> None:
        """Stream validated models into target database tables via an IngestionSpec.

        :param items: Iterable of validated Pydantic model instances.
        :type items: Iterable[T]
        :param spec: Declarative ingestion specification resolving destination schema.
        :type spec: IngestionSpec[T]
        """
        rows = (spec.row_factory(item) for item in items)
        self._loader.load(
            table_name=spec.table_name,
            columns=spec.columns,
            rows=rows,
        )

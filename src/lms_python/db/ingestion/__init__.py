"""Ingestion components and schema specifications."""

from lms_python.db.ingestion.ingestor import DataIngestor
from lms_python.db.ingestion.protocols import DataLoader
from lms_python.db.ingestion.spec import ROOM_SPEC, STUDENT_SPEC, IngestionSpec

__all__ = [
    "ROOM_SPEC",
    "STUDENT_SPEC",
    "DataIngestor",
    "DataLoader",
    "IngestionSpec",
]

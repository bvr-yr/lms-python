"""Bulk data ingestion handling."""

import logging
from collections.abc import Iterable, Sequence
from typing import Protocol

from lms_python.logger import perf_logger
from lms_python.models.source import Room, Student

logger = logging.getLogger(__name__)


class DataLoader(Protocol):
    """Structural interface specifying data loading capabilities."""

    def load(
        self,
        table_name: str,
        *,
        columns: Sequence[str],
        rows: Iterable[Sequence[object]],
    ) -> None:
        """Stream tabular records into a target table.

        :param table_name: Destination database table name.
        :type table_name: str
        :param columns: (keyword-only) Column names matching the positional order of row values.
        :type columns: Sequence[str]
        :param columns: (keyword-only) Iterable yielding ordered sequences of column values.
        :type rows: Iterable[Sequence[object]]
        """


class DataIngestor:
    """Maps validated Pydantic models to database rows for bulk loading."""

    def __init__(self, loader: DataLoader) -> None:
        """Initialize the ingestor.

        :param loader: Configured DatabaseLoader instance.
        :type loader: DatabaseLoader
        """
        self._loader = loader

    @perf_logger
    def insert_rooms(self, rooms: Iterable[Room]) -> None:
        """Extract fields from Room models and stream them to the table.

        :param rooms: Iterable of validated Room instances.
        :type rooms: Iterable[Room]
        """
        columns = ("id", "room_name")
        rows = ((room.id, room.name) for room in rooms)
        self._loader.load(table_name="rooms", columns=columns, rows=rows)

    @perf_logger
    def insert_students(self, students: Iterable[Student]) -> None:
        """Extract fields from Student models and stream them to the table.

        :param students: Iterable of validated Student instances.
        :type students: Iterable[Student]
        """
        columns = ("id", "full_name", "birthday", "gender", "room_id")
        rows = (
            (
                student.id,
                student.name,
                student.birthday,
                student.sex,
                student.room,
            )
            for student in students
        )
        self._loader.load(table_name="students", columns=columns, rows=rows)

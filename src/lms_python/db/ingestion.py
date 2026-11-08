"""Bulk data ingestion handling."""

import logging
from collections.abc import Iterable

from lms_python.db.loader import DatabaseLoader
from lms_python.logger import perf_logger
from lms_python.models.source import Room, Student

logger = logging.getLogger(__name__)


class DataIngestor:
    """Maps validated Pydantic models to database rows for bulk loading."""

    def __init__(self, loader: DatabaseLoader) -> None:
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
        self._loader.copy_batch(table_name="rooms", columns=columns, rows=rows)

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
        self._loader.copy_batch(table_name="students", columns=columns, rows=rows)

import logging
from collections.abc import Iterable

from lms_python.db.loader import DatabaseLoader
from lms_python.logger import perf_logger
from lms_python.models.source import Room, Student

logger = logging.getLogger(__name__)


class DataIngestor:
    def __init__(self, loader: DatabaseLoader) -> None:
        self._loader = loader

    @perf_logger
    def insert_rooms(self, rooms: Iterable[Room]) -> None:
        columns = ("id", "room_name")
        rows = ((room.id, room.name) for room in rooms)
        self._loader.copy_batch("rooms", columns, rows)

    @perf_logger
    def insert_students(self, students: Iterable[Student]) -> None:
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
        self._loader.copy_batch("students", columns, rows)

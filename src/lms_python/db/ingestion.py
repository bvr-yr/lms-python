from collections.abc import Iterable

from lms_python.db.loader import DatabaseLoader
from lms_python.models.source import Room, Student


class DataIngestor:
    def __init__(self, loader: DatabaseLoader) -> None:
        self._loader = loader

    def insert_rooms(self, rooms: Iterable[Room]) -> None:
        columns = ("id", "room_name")
        rows = ((room.id, room.name) for room in rooms)
        self._loader._copy_batch("rooms", columns, rows)

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
        self._loader._copy_batch("students", columns, rows)

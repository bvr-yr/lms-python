from typing import Any

from psycopg import Connection

from lms_python.db.loader import DatabaseLoader


class StudentRepository:
    def __init__(self, connection: Connection, loader: DatabaseLoader) -> None:
        self._conn = connection
        self._loader = loader

    def insert_rooms(self, rooms: list[dict[str, Any]]) -> None:
        columns = ["id", "room_name"]
        rows = [(room["id"], room["name"]) for room in rooms]
        self._loader.copy_batch("rooms", columns, rows)

    def insert_students(self, students: list[dict[str, Any]]) -> None:
        columns = ["id", "full_name", "birthday", "gender", "room_id"]
        rows = [
            (
                student["id"],
                student["name"],
                student["birthday"],
                student["sex"],
                student["room"],
            )
            for student in students
        ]
        self._loader.copy_batch("students", columns, rows)

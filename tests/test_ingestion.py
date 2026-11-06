import unittest
from datetime import datetime
from unittest.mock import MagicMock

from lms_python.db.ingestion import DataIngestor
from lms_python.db.loader import DatabaseLoader
from lms_python.models.source import Room, Student


class TestDataIngestor(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_loader = MagicMock(spec=DatabaseLoader)
        self.ingestor = DataIngestor(self.mock_loader)

    def test_insert_rooms_mapping(self) -> None:
        rooms = [Room(id=1, name="Room #1"), Room(id=2, name="Room #2")]
        self.ingestor.insert_rooms(rooms)

        self.mock_loader.copy_batch.assert_called_once()
        table_name, columns, rows_gen = self.mock_loader.copy_batch.call_args[0]

        self.assertEqual(table_name, "rooms")
        self.assertEqual(columns, ("id", "room_name"))
        self.assertEqual(list(rows_gen), [(1, "Room #1"), (2, "Room #2")])

    def test_insert_students_mapping(self) -> None:
        now = datetime(2000, 1, 1, 0, 0)
        students = [Student(id=1, name="Alice", birthday=now, room=10, sex="F")]
        self.ingestor.insert_students(students)

        self.mock_loader.copy_batch.assert_called_once()
        table_name, columns, rows_gen = self.mock_loader.copy_batch.call_args[0]

        self.assertEqual(table_name, "students")
        self.assertEqual(columns, ("id", "full_name", "birthday", "gender", "room_id"))
        self.assertEqual(list(rows_gen), [(1, "Alice", now, "F", 10)])

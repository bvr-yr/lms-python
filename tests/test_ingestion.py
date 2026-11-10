from datetime import datetime
from unittest.mock import MagicMock

from lms_python.db.ingestion.ingestor import DataIngestor
from lms_python.db.ingestion.protocols import DataLoader
from lms_python.db.ingestion.spec import ROOM_SPEC, STUDENT_SPEC
from lms_python.models.source import Room, Student


def test_insert_rooms_mapping():
    mock_loader = MagicMock(spec=DataLoader)
    ingestor = DataIngestor(mock_loader)

    rooms = [Room(id=1, name="Room 1"), Room(id=2, name="Room 2")]
    ingestor.insert(rooms, ROOM_SPEC)

    mock_loader.load.assert_called_once()
    kwargs = mock_loader.load.call_args.kwargs

    table_name = kwargs["table_name"]
    columns = kwargs["columns"]
    rows = list(kwargs["rows"])

    assert table_name == "rooms"
    assert columns == ("id", "room_name")
    assert rows == [(1, "Room 1"), (2, "Room 2")]


def test_insert_students_mapping():
    mock_loader = MagicMock(spec=DataLoader)
    ingestor = DataIngestor(mock_loader)

    now = datetime(2000, 1, 1, 0, 0)
    students = [Student(id=1, name="Alice", birthday=now, room=10, sex="F")]
    ingestor.insert(students, STUDENT_SPEC)

    mock_loader.load.assert_called_once()
    kwargs = mock_loader.load.call_args.kwargs

    table_name = kwargs["table_name"]
    columns = kwargs["columns"]
    rows = list(kwargs["rows"])

    assert table_name == "students"
    assert columns == ("id", "full_name", "birthday", "gender", "room_id")
    assert rows == [(1, "Alice", now, "F", 10)]

import pytest
from pydantic import ValidationError

from lms_python.models.source import Room
from lms_python.readers.json import JSONReader


def test_json_reader_valid_data(tmp_path):
    file_path = tmp_path / "rooms.json"
    file_path.write_text(
        '[{"id": 1, "name": "Room A"}, {"id": 2, "name": "Room B"}]', encoding="utf-8"
    )

    rooms = list(JSONReader().get(file_path, Room))

    assert len(rooms) == 2
    assert rooms[0].id == 1
    assert rooms[1].name == "Room B"


def test_json_reader_file_not_found(tmp_path):
    file_path = tmp_path / "fake.json"

    with pytest.raises(FileNotFoundError):
        list(JSONReader().get(file_path, Room))


def test_json_reader_invalid_schema(tmp_path):
    file_path = tmp_path / "bad_schema.json"
    file_path.write_text('[{"id": "one", "name": "Room A"}]', encoding="utf-8")

    with pytest.raises(ValidationError):
        list(JSONReader().get(file_path, Room))

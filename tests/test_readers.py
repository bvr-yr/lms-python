import tempfile
import unittest
from pathlib import Path

from pydantic import ValidationError

from lms_python.models.source import Room
from lms_python.readers.json import JSONReader


class TestJSONReader(unittest.TestCase):
    def setUp(self) -> None:
        self.reader = JSONReader()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.dir_path = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_read_valid_json(self) -> None:
        file_path = self.dir_path / "rooms.json"
        file_path.write_text('[{"id": 1, "name": "Room #1"}]', encoding="utf-8")

        rooms = list(self.reader.get(file_path, Room))

        self.assertEqual(len(rooms), 1)
        self.assertEqual(rooms[0].id, 1)
        self.assertEqual(rooms[0].name, "Room #1")

    def test_file_not_found(self) -> None:
        missing_path = self.dir_path / "non_existent.json"
        with self.assertRaises(FileNotFoundError):
            list(self.reader.get(missing_path, Room))

    def test_non_list_json_raises_type_error(self) -> None:
        file_path = self.dir_path / "not_a_list.json"
        file_path.write_text('{"id": 1, "name": "Room #1"}', encoding="utf-8")

        with self.assertRaises(TypeError):
            list(self.reader.get(file_path, Room))

    def test_invalid_schema_raises_validation_error(self) -> None:
        file_path = self.dir_path / "invalid_schema.json"
        file_path.write_text(
            '[{"id": "invalid_id", "name": "Room #1"}]', encoding="utf-8"
        )

        with self.assertRaises(ValidationError):
            list(self.reader.get(file_path, Room))

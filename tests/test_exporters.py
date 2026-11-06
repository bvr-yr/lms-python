import json
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from lms_python.exporters.json import JSONExporter
from lms_python.exporters.xml import XMLExporter
from lms_python.models.queries import RoomStudentCount


class TestExporters(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.dir_path = Path(self.temp_dir.name)
        self.sample_data = [
            RoomStudentCount(room_id=10, room_name="Room #10", students_count=5)
        ]

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_json_exporter(self) -> None:
        out_file = self.dir_path / "result.json"
        JSONExporter().export(self.sample_data, out_file)

        self.assertTrue(out_file.is_file())
        with out_file.open("r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertEqual(
            data, [{"room_id": 10, "room_name": "Room #10", "students_count": 5}]
        )

    def test_xml_exporter(self) -> None:
        out_file = self.dir_path / "result.xml"
        XMLExporter().export(self.sample_data, out_file)

        self.assertTrue(out_file.is_file())
        tree = ET.parse(out_file)
        root = tree.getroot()

        self.assertEqual(root.tag, "results")
        item = root.find("item")
        self.assertIsNotNone(item)
        self.assertEqual(item.findtext("room_id"), "10")  # ty: ignore[unresolved-attribute]
        self.assertEqual(item.findtext("room_name"), "Room #10")  # ty: ignore[unresolved-attribute]
        self.assertEqual(item.findtext("students_count"), "5")  # ty: ignore[unresolved-attribute]

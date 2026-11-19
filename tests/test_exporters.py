import json
import xml.etree.ElementTree as ET

import pytest

from lms_python.exporters.json import JSONExporter
from lms_python.exporters.xml import XMLExporter
from lms_python.models.queries import RoomStudentCount


@pytest.fixture
def sample_data():
    return [
        RoomStudentCount(room_id=10, room_name="Room #10", students_count=5),
        RoomStudentCount(room_id=20, room_name="Room #20", students_count=0),
    ]


def test_json_exporter(tmp_path, sample_data):
    out = tmp_path / "out.json"
    JSONExporter().export(sample_data, out)

    assert out.is_file()

    data = json.loads(out.read_text(encoding="utf-8"))
    assert len(data) == 2
    assert data[0]["room_id"] == 10
    assert data[1]["students_count"] == 0


def test_xml_exporter(tmp_path, sample_data):
    out = tmp_path / "out.xml"
    XMLExporter().export(sample_data, out)

    assert out.is_file()

    tree = ET.parse(out)
    root = tree.getroot()

    assert root.tag == "results"
    items = root.findall("item")
    assert len(items) == 2
    assert items[0].findtext("room_id") == "10"
    assert items[0].findtext("room_name") == "Room #10"

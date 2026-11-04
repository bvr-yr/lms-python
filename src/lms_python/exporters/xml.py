import xml.etree.ElementTree as ET
from collections.abc import Sequence
from pathlib import Path

from pydantic import BaseModel

from lms_python.exporters.base import BaseExporter


class XMLExporter(BaseExporter):
    def _write(self, data: Sequence[BaseModel], path: Path) -> None:
        root = ET.Element("results")

        for item in data:
            item_elem = ET.SubElement(root, "item")
            for key, value in item.model_dump().items():
                child = ET.SubElement(item_elem, str(key))
                child.text = str(value)

        ET.indent(root, space="    ", level=0)

        tree = ET.ElementTree(root)
        with path.open("wb") as file:
            tree.write(file, encoding="utf-8", xml_declaration=True)

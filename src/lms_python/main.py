import argparse
from pathlib import Path

from lms_python.db.analytics import DataAnalytics
from lms_python.db.connection import connection_manager
from lms_python.db.ingestion import DataIngestor
from lms_python.db.loader import DatabaseLoader
from lms_python.db.schema import SchemaManager
from lms_python.exporters.json import JSONExporter
from lms_python.exporters.xml import XMLExporter
from lms_python.models import Room, Student
from lms_python.readers.json import JSONReader

EXPORTERS = {
    "json": JSONExporter(),
    "xml": XMLExporter(),
}

OUTPUT_DIR = Path("output")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="LMS Python task")
    parser.add_argument(
        "-s", "--students", required=True, help="Path to students JSON file"
    )
    parser.add_argument("-r", "--rooms", required=True, help="Path to rooms JSON file")
    parser.add_argument(
        "-f",
        "--format",
        required=False,
        default="json",
        choices=EXPORTERS.keys(),
        help="Output format",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    reader = JSONReader()
    rooms_data = reader.get(args.rooms, Room)
    students_data = reader.get(args.students, Student)

    with connection_manager.get_connection() as connection:
        with connection.transaction():
            schema = SchemaManager(connection)
            schema.create_tables()
            schema.truncate_tables()

            loader = DatabaseLoader(connection)
            ingestor = DataIngestor(loader)
            ingestor.insert_rooms(rooms_data)
            ingestor.insert_students(students_data)
            schema.create_index()

        analytics = DataAnalytics(connection)
        reports = analytics.execute_reports()

    exporter = EXPORTERS[args.format]
    for report_name, data in reports.items():
        output_path = OUTPUT_DIR / f"{report_name}.{args.format}"
        exporter.export(data, output_path)


if __name__ == "__main__":
    main()

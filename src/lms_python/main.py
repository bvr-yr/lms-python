import argparse

from lms_python.db.connection import connection_manager
from lms_python.db.ingestion import DataIngestor
from lms_python.db.schema import SchemaManager
from lms_python.models import Room, Student
from lms_python.readers.json import JSONReader


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="LMS Python task")
    parser.add_argument(
        "-s", "--students", required=True, help="Path to students JSON file"
    )
    parser.add_argument("-r", "--rooms", required=True, help="Path to rooms JSON file")
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

            ingestor = DataIngestor(connection)
            ingestor.insert_rooms(rooms_data)
            ingestor.insert_students(students_data)
            schema.create_index()


if __name__ == "__main__":
    main()

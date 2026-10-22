from pathlib import Path
from pprint import pprint

from lms_python.db.connection import connection_manager
from lms_python.db.loader import DatabaseLoader
from lms_python.db.repository import StudentRepository
from lms_python.db.schema import SchemaManager
from lms_python.reader import JSONReader


def main() -> None:

    def print_header(header: str) -> None:
        char = "="
        print(f"\n{char * 10} {header} {char * (33 - len(header))}")

    print_header("READER TEST")
    reader = JSONReader()

    data_dir = Path(__file__).parent / "data"
    rooms_path = data_dir / "rooms.json"
    students_path = data_dir / "students.json"

    rooms = reader.read(rooms_path)
    students = reader.read(students_path)

    print(f"records: rooms:{len(rooms)}, students:{len(students)}")

    for t in rooms, students:
        print()
        pprint(t[:5])  # noqa: T203

    print_header("DB OPERATIONS TESTS")
    # INFO: https://docs.astral.sh/ruff/rules/multiple-with-statements/
    with connection_manager.get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            print(f"version: {cursor.fetchone()}")

        with connection.transaction():
            schema = SchemaManager(connection)
            schema.create_tables()

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                """,
            )
            print(f"tables: {cursor.fetchall()}")

        with connection.transaction():
            schema = SchemaManager(connection)
            loader = DatabaseLoader(connection)
            repo = StudentRepository(connection, loader)

            schema.truncate_tables()
            repo.insert_rooms(rooms)
            repo.insert_students(students)

        with connection.cursor() as cursor:
            cursor.execute("SELECT count(*) FROM rooms;")
            rooms_count = cursor.fetchone()

            cursor.execute("SELECT count(*) FROM students;")
            students_count = cursor.fetchone()

            print(f"rows: rooms:{rooms_count}, students: {students_count}")


if __name__ == "__main__":
    main()

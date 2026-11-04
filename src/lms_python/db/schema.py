from psycopg import Connection

from lms_python.db.resources import load_sql_resource


class SchemaManager:
    def __init__(self, connection: Connection) -> None:
        self._conn = connection

    def create_tables(self) -> None:
        query = load_sql_resource("lms_python.sql", "create_tables.sql")
        with self._conn.cursor() as cursor:
            cursor.execute(query)

    def truncate_tables(self) -> None:
        with self._conn.cursor() as cursor:
            cursor.execute("DROP INDEX IF EXISTS idx_students_room_id;")
            cursor.execute("TRUNCATE TABLE students, rooms RESTART IDENTITY CASCADE;")

    def create_index(self) -> None:
        with self._conn.cursor() as cursor:
            cursor.execute("CREATE INDEX idx_students_room_id ON students (room_id);")

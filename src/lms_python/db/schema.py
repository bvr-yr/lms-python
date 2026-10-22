from psycopg import Connection

from lms_python.db.utils import load_sql_resource


class SchemaManager:
    def __init__(self, connection: Connection) -> None:
        self._conn = connection

    def create_tables(self) -> None:
        query = load_sql_resource("lms_python.sql", "create_tables.sql")
        with self._conn.cursor() as cursor:
            cursor.execute(query)

    def truncate_tables(self) -> None:
        with self._conn.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE students, rooms RESTART IDENTITY CASCADE;")

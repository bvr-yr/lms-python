from collections.abc import Iterable, Sequence

from psycopg import Connection, sql

from lms_python.models import Room, Student


class DataIngestor:
    def __init__(self, connection: Connection) -> None:
        self._conn = connection

    def _copy_batch(
        self,
        table_name: str,
        columns: Sequence[str],
        rows: Iterable[Sequence[object]],
    ) -> None:
        copy_sql = sql.SQL("COPY {table} ({fields}) FROM STDIN").format(
            table=sql.Identifier(table_name),
            fields=sql.SQL(", ").join(sql.Identifier(col) for col in columns),
        )

        with self._conn.cursor() as cursor, cursor.copy(copy_sql) as copy:
            for row in rows:
                copy.write_row(row)

    def insert_rooms(self, rooms: Iterable[Room]) -> None:
        columns = ("id", "room_name")
        rows = ((room.id, room.name) for room in rooms)
        self._copy_batch("rooms", columns, rows)

    def insert_students(self, students: Iterable[Student]) -> None:
        columns = ("id", "full_name", "birthday", "gender", "room_id")
        rows = (
            (
                student.id,
                student.name,
                student.birthday,
                student.sex,
                student.room,
            )
            for student in students
        )
        self._copy_batch("students", columns, rows)

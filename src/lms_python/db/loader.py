from collections.abc import Iterable, Sequence

from psycopg import Connection, sql


class DatabaseLoader:
    def __init__(self, connection: Connection) -> None:
        self._conn = connection

    def copy_batch(
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

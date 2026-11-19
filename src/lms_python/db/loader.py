"""Data loading utilities."""

import logging
from collections.abc import Iterable, Sequence

from psycopg import Connection, sql

logger = logging.getLogger(__name__)


class PostgresLoader:
    """Manages data loading using PostgreSQL COPY streaming."""

    def __init__(self, connection: Connection) -> None:
        """Initialize the loader with an open database connection.

        :param connection: Active psycopg connection.
        :type connection: Connection
        """
        self._conn = connection

    def load(
        self,
        table_name: str,
        *,
        columns: Sequence[str],
        rows: Iterable[Sequence[object]],
    ) -> None:
        """Stream in-memory rows directly into a table via COPY FROM STDIN.

        :param table_name: Destination PostgreSQL table name.
        :type table_name: str
        :param columns: (keyword-only) Column names matching the positional order of row tuples.
        :type columns: Sequence[str]
        :param rows: (keyword-only) Iterable yielding ordered sequences of column values.
        :type rows: Iterable[Sequence[object]]
        """
        copy_sql = sql.SQL("COPY {table} ({fields}) FROM STDIN").format(
            table=sql.Identifier(table_name),
            fields=sql.SQL(", ").join(sql.Identifier(col) for col in columns),
        )

        count = 0
        with self._conn.cursor() as cursor, cursor.copy(copy_sql) as copy:
            for row in rows:
                copy.write_row(row)
                count += 1

        logger.info("loaded %d records into table '%s'", count, table_name)

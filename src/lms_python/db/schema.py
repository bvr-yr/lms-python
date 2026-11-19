"""Database schema definition and lifecycle management."""

import logging

from psycopg import Connection

from lms_python.db.resources import load_sql_resource

logger = logging.getLogger(__name__)

SQL_PACKAGE = "lms_python.sql"


class SchemaManager:
    """Executes DDL operations managing database table and index lifecycles."""

    def __init__(self, connection: Connection) -> None:
        """Initialize the schema manager.

        :param connection: Active psycopg PostgreSQL connection.
        :type connection: Connection
        """
        self._conn = connection

    def create_tables(self) -> None:
        """Execute baseline DDL statements to create rooms and students tables."""
        sql_filename = "create_tables.sql"
        query = load_sql_resource(SQL_PACKAGE, sql_filename)
        with self._conn.cursor() as cursor:
            cursor.execute(query)
            logger.info("created tables with %s", sql_filename)

    def truncate_tables(self) -> None:
        """Drop dependent indexes and truncate tables with sequence restarts."""
        with self._conn.cursor() as cursor:
            cursor.execute("DROP INDEX IF EXISTS idx_students_room_id;")
            logger.info("dropped index")
            cursor.execute("TRUNCATE TABLE students, rooms RESTART IDENTITY CASCADE;")
            logger.info("truncated tables")

    def create_index(self) -> None:
        """Execute DDL statement to create index on the students table foreign key column (room_id)."""
        sql_filename = "create_index.sql"
        query = load_sql_resource(SQL_PACKAGE, sql_filename)
        with self._conn.cursor() as cursor:
            cursor.execute(query)
            logger.info("created index with %s", sql_filename)

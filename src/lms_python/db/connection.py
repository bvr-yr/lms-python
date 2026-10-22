from collections.abc import Generator
from contextlib import contextmanager

import psycopg
from psycopg import Connection

from lms_python.config import settings


class ConnectionManager:
    def __init__(self, dsn: str | None = None) -> None:
        self._dsn = dsn or settings.dsn

    @contextmanager
    def get_connection(self) -> Generator[Connection]:
        with psycopg.connect(self._dsn) as connection:
            yield connection


connection_manager = ConnectionManager()

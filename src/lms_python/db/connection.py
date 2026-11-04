from collections.abc import Generator
from contextlib import contextmanager

import psycopg
from psycopg import Connection

from lms_python.config import ConnectionParams, settings


class ConnectionManager:
    def __init__(self, connections_params: ConnectionParams) -> None:
        self._params = connections_params

    @contextmanager
    def get_connection(self) -> Generator[Connection]:
        with psycopg.connect(**self._params) as connection:
            yield connection


connection_manager = ConnectionManager(settings.connection_params)

import logging
from collections.abc import Generator
from contextlib import contextmanager

import psycopg
from psycopg import Connection

from lms_python.config import ConnectionParams, db_settings

logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self, connections_params: ConnectionParams) -> None:
        self._params = connections_params

    @contextmanager
    def get_connection(self) -> Generator[Connection]:
        logger.info(
            "connecting to PostgreSQL at %s:%s/%s (user: %s)",
            self._params["host"],
            self._params["port"],
            self._params["dbname"],
            self._params["user"],
        )
        with psycopg.connect(**self._params) as connection:
            logger.info("succesfully connected")
            yield connection

        logger.info("disconnected")


connection_manager = ConnectionManager(db_settings.connection_params)

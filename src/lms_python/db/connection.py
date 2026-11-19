"""PostgreSQL connection management and context injection."""

import logging
from collections.abc import Generator
from contextlib import contextmanager

import psycopg
from psycopg import Connection

from lms_python.config import ConnectionParams, db_settings

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages the creation and lifecycle of direct PostgreSQL connections."""

    def __init__(self, connections_params: ConnectionParams) -> None:
        """Initialize the connection manager with database parameters.

        :param connections_params: PostgreSQL connection parameters.
        :type connections_params: ConnectionParams
        """
        self._params = connections_params

    @contextmanager
    def get_connection(self) -> Generator[Connection]:
        """Open a dedicated database connection and close it upon context exit.

        :return: Context manager yielding an active psycopg connection.
        :rtype: Generator[Connection]
        :raises psycopg.OperationalError: If the database is unreachable or credentials fail.
        """
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

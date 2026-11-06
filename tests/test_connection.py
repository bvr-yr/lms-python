import unittest
from unittest.mock import MagicMock, patch

import psycopg

from lms_python.config import ConnectionParams
from lms_python.db.connection import ConnectionManager


class TestConnectionManager(unittest.TestCase):
    def setUp(self) -> None:
        self.params: ConnectionParams = {
            "host": "localhost",
            "port": 5432,
            "dbname": "test_db",
            "user": "test_user",
            "password": "secret_password",
        }
        self.manager = ConnectionManager(self.params)

    @patch("psycopg.connect")
    def test_get_connection_success(self, mock_connect: MagicMock) -> None:
        mock_conn = MagicMock(spec=psycopg.Connection)
        mock_connect.return_value.__enter__.return_value = mock_conn

        with self.manager.get_connection() as conn:
            self.assertEqual(conn, mock_conn)

        mock_connect.assert_called_once_with(**self.params)

    @patch("psycopg.connect")
    def test_get_connection_failure(self, mock_connect: MagicMock) -> None:
        mock_connect.side_effect = psycopg.OperationalError("Connection refused")

        with self.assertRaises(psycopg.OperationalError), self.manager.get_connection():
            pass

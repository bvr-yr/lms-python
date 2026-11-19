import os

import pytest

from lms_python.db.connection import connection_manager


@pytest.mark.skipif(
    os.getenv("TEST_LIVE_DB") != "1",
    reason="TEST_LIVE_DB=1 to run",
)
def test_live_database_connection():
    with connection_manager.get_connection() as conn, conn.cursor() as cursor:
        cursor.execute("SELECT 1;")
        result = cursor.fetchone()

        assert result == (1,)

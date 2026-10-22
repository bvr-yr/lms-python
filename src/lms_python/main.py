from lms_python.db.connection import connection_manager
from lms_python.db.schema import SchemaManager


def main() -> None:
    print("====== SMOKE TEST ======")
    # INFO: https://docs.astral.sh/ruff/rules/multiple-with-statements/
    with connection_manager.get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            print(f"version: {cursor.fetchone()}")

        with connection.transaction():
            schema = SchemaManager(connection)
            schema.create_tables()

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                """,
            )
            print(f"tables: {cursor.fetchall()}")


if __name__ == "__main__":
    main()

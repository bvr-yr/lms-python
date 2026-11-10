"""Application entry point and CLI orchestration."""

import argparse
import logging
import sys
from pathlib import Path

import psycopg
from pydantic import ValidationError

from lms_python.db.analytics import DataAnalyticsService
from lms_python.db.connection import connection_manager
from lms_python.db.ingestion.ingestor import DataIngestor
from lms_python.db.ingestion.spec import ROOM_SPEC, STUDENT_SPEC
from lms_python.db.loader import PostgresLoader
from lms_python.db.schema import SchemaManager
from lms_python.exporters.json import JSONExporter
from lms_python.exporters.xml import XMLExporter
from lms_python.logger import setup_logging, timer
from lms_python.models.source import Room, Student
from lms_python.readers.json import JSONReader

logger = logging.getLogger(__name__)

EXPORTERS = {
    "json": JSONExporter(),
    "xml": XMLExporter(),
}

OUTPUT_DIR = Path("output")


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments.

    :return: Parsed CLI arguments.
    :rtype: argparse.Namespace
    """
    parser = argparse.ArgumentParser(description="LMS Python task")
    parser.add_argument(
        "-s", "--students", required=True, help="Path to students JSON file"
    )
    parser.add_argument("-r", "--rooms", required=True, help="Path to rooms JSON file")
    parser.add_argument(
        "-f",
        "--format",
        required=False,
        default="json",
        choices=EXPORTERS.keys(),
        help="Output format",
    )
    return parser.parse_args()


def main() -> int:
    """Execute the main ETL pipeline orchestration.

    :return: Process exit status code (0 for success, 1 for failure).
    :rtype: int
    """
    setup_logging()
    args = parse_args()

    try:
        reader = JSONReader()
        rooms_data = reader.get(args.rooms, Room)
        students_data = reader.get(args.students, Student)

        with connection_manager.get_connection() as connection:
            with connection.transaction():
                schema = SchemaManager(connection)
                schema.create_tables()
                schema.truncate_tables()

                loader = PostgresLoader(connection)
                ingestor = DataIngestor(loader)

                with timer("ingestion"):
                    ingestor.insert(rooms_data, ROOM_SPEC)
                    ingestor.insert(students_data, STUDENT_SPEC)

                schema.create_index()

            analytics = DataAnalyticsService(connection)
            reports = analytics.execute_reports()

        exporter = EXPORTERS[args.format]
        for report_name, data in reports.items():
            output_path = OUTPUT_DIR / f"{report_name}.{args.format}"
            exporter.export(data, output_path)

        return 0

    except FileNotFoundError as e:
        logger.error("input error: %s", e)
    except TypeError as e:
        logger.error("invalid type: %s", e)
    except ValidationError as e:
        logger.error("validation error:\n%s", e)
    except psycopg.OperationalError as e:
        logger.error("db operational error: %s", e)
    except psycopg.DatabaseError as e:
        logger.error("db error: %s", e)
    except Exception:
        logger.exception("unexpected error")

    return 1


if __name__ == "__main__":
    sys.exit(main())

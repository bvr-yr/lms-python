"""Analytical query execution and validation."""

import logging
from collections.abc import Iterable

from psycopg import Connection
from psycopg.rows import dict_row
from pydantic import BaseModel

from lms_python.db.resources import load_sql_resource
from lms_python.logger import perf_logger
from lms_python.models.report import AnalyticsReport

logger = logging.getLogger(__name__)


class DataAnalyticsService:
    """Orchestrates execution of SQL analytical queries and validates recordsets."""

    def __init__(self, connection: Connection) -> None:
        """Initialize the analytics service with an active connection.

        :param connection: Active psycopg connection with dict_row cursor support.
        :type connection: Connection
        """
        self._conn = connection

    def execute_query[T: BaseModel](self, sql_filename: str, model: type[T]) -> list[T]:
        """Execute a bundled SQL query file and validate result rows into Pydantic model instances.

        :param sql_filename: SQL file name located within the analytics resource package.
        :type sql_filename: str
        :param model: Pydantic model class validating each result dictionary.
        :type model: type[T]
        :return: List of validated model instances.
        :rtype: list[T]
        :raises pydantic.ValidationError: If query result columns fail model schema validation.
        """
        query = load_sql_resource("lms_python.sql.analytics", sql_filename)
        with self._conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(query)
            models = [model.model_validate(row) for row in cursor.fetchall()]
            logger.info("executed %s: %d rows", sql_filename, len(models))
            return models

    @perf_logger
    def execute_one(
        self,
        report: AnalyticsReport,
    ) -> list[BaseModel]:
        """Execute a single analytics report.

        :param report: AnalyticsReport enum defining the query and model.
        :type report: AnalyticsReport
        :return: Validated resultset.
        :rtype: list[BaseModel]
        """
        return self.execute_query(report.filename, report.model)

    @perf_logger
    def execute_reports(
        self,
        reports: Iterable[AnalyticsReport] = AnalyticsReport,
    ) -> dict[str, list[BaseModel]]:
        """Execute a batch of analytics reports.

        :param reports: Iterable of AnalyticsReport enums.
        :type reports: Iterable[AnalyticsReport]
        :return: Dictionary mapping report names to validated resultsets.
        :rtype: dict[str, list[BaseModel]]
        """
        return {
            report.report_name: self.execute_query(report.filename, report.model)
            for report in reports
        }

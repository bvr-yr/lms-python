import logging
from collections.abc import Iterable

from psycopg import Connection
from psycopg.rows import dict_row
from pydantic import BaseModel

from lms_python.db.resources import load_sql_resource
from lms_python.logger import perf_logger
from lms_python.models.report import AnalyticsReport

logger = logging.getLogger(__name__)


class DataAnalytics:
    def __init__(self, connection: Connection) -> None:
        self._conn = connection

    def execute_query[T: BaseModel](self, sql_filename: str, model: type[T]) -> list[T]:
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
        return self.execute_query(report.filename, report.model)

    @perf_logger
    def execute_reports(
        self,
        reports: Iterable[AnalyticsReport] = AnalyticsReport,
    ) -> dict[str, list[BaseModel]]:
        return {
            report.report_name: self.execute_query(report.filename, report.model)
            for report in reports
        }

from collections.abc import Iterable
from enum import Enum

from psycopg import Connection
from psycopg.rows import dict_row
from pydantic import BaseModel

from lms_python.db.resources import load_sql_resource
from lms_python.models import (
    DiverseGenderRoom,
    RoomAgeDiff,
    RoomAvgAge,
    RoomStudentCount,
)


class AnalyticsReport(Enum):
    ROOMS_LIST = ("1_rooms_list.sql", RoomStudentCount)
    TOP5_MIN_AVG = ("2_top5_min_avg.sql", RoomAvgAge)
    TOP5_MAX_AGE_DIFF = ("3_top5_max_age_diff.sql", RoomAgeDiff)
    ROOMS_LIST_DIFF_GENDER = ("4_rooms_list_diff_gender.sql", DiverseGenderRoom)

    def __init__(self, filename: str, model: type[BaseModel]) -> None:
        self.filename = filename
        self.model = model

    @property
    def report_name(self) -> str:
        return self.name.lower()

    @property
    def report_name_as_filename(self) -> str:
        return self.filename.removesuffix(".sql")


class DataAnalytics:
    def __init__(self, connection: Connection) -> None:
        self._conn = connection

    def execute_query[T: BaseModel](self, sql_filename: str, model: type[T]) -> list[T]:
        query = load_sql_resource("lms_python.sql.analytics", sql_filename)
        with self._conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(query)
            return [model.model_validate(row) for row in cursor.fetchall()]

    def execute_one(
        self,
        report: AnalyticsReport,
    ) -> list[BaseModel]:
        return self.execute_query(report.filename, report.model)

    def execute_reports(
        self,
        reports: Iterable[AnalyticsReport] = AnalyticsReport,
    ) -> dict[str, list[BaseModel]]:
        return {
            report.report_name: self.execute_query(report.filename, report.model)
            for report in reports
        }

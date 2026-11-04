from enum import Enum

from pydantic import BaseModel

from lms_python.models.queries import (
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

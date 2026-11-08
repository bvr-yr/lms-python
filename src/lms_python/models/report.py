"""Enum definitions mapping SQL files to their respective Pydantic models."""

from enum import Enum

from pydantic import BaseModel

from lms_python.models.queries import (
    DiverseGenderRoom,
    RoomAgeDiff,
    RoomAvgAge,
    RoomStudentCount,
)


class AnalyticsReport(Enum):
    """Registry of available analytics reports linking SQL resources to validation models."""

    ROOMS_LIST = ("1_rooms_list.sql", RoomStudentCount)
    TOP5_MIN_AVG = ("2_top5_min_avg.sql", RoomAvgAge)
    TOP5_MAX_AGE_DIFF = ("3_top5_max_age_diff.sql", RoomAgeDiff)
    ROOMS_LIST_DIFF_GENDER = ("4_rooms_list_diff_gender.sql", DiverseGenderRoom)

    def __init__(self, filename: str, model: type[BaseModel]) -> None:
        """Initialize the report enum member.

        :param filename: Target SQL resource file name.
        :type filename: str
        :param model: Target Pydantic model for row validation.
        :type model: type[BaseModel]
        """
        self.filename = filename
        self.model = model

    @property
    def report_name(self) -> str:
        """Lowercase enum member name as the report identifier.

        :return: Lowercase report name.
        :rtype: str
        """
        return self.name.lower()

    @property
    def report_name_as_filename(self) -> str:
        """Stripped SQL filename without extension as the report identifier.

        :return: Base filename report name.
        :rtype: str
        """
        return self.filename.removesuffix(".sql")

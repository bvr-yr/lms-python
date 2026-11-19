"""Pydantic models representing analytical query resultsets."""

from pydantic import BaseModel


class RoomStudentCount(BaseModel):
    """Schema for student counts per room query results."""

    room_id: int
    room_name: str
    students_count: int


class RoomAvgAge(BaseModel):
    """Schema for average student age per room query results."""

    room_id: int
    room_name: str
    avg_student_age: float


class RoomAgeDiff(BaseModel):
    """Schema for maximum student age difference per room query results."""

    room_id: int
    room_name: str
    age_diff: int


class DiverseGenderRoom(BaseModel):
    """Schema for mixed gender room query results."""

    room_id: int
    room_name: str

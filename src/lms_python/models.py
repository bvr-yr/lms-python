from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class Room(BaseModel):
    id: int
    name: str


class Student(BaseModel):
    id: int
    name: str
    birthday: datetime
    room: int
    sex: Literal["M", "F"]


class RoomStudentCount(BaseModel):
    room_id: int
    room_name: str
    students_count: int


class RoomAvgAge(BaseModel):
    room_id: int
    room_name: str
    avg_student_age: float


class RoomAgeDiff(BaseModel):
    room_id: int
    room_name: str
    age_diff: int


class DiverseGenderRoom(BaseModel):
    room_id: int
    room_name: str

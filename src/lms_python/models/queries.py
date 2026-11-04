from pydantic import BaseModel


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

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

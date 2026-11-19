"""Pydantic models representing raw source data payloads."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class Room(BaseModel):
    """Source schema definition for Room payloads."""

    id: int
    name: str


class Student(BaseModel):
    """Source schema definition for Student payloads."""

    id: int
    name: str
    birthday: datetime
    room: int
    sex: Literal["M", "F"]

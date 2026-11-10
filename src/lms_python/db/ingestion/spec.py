"""Declarative ingestion mapping specifications."""

from collections.abc import Callable, Sequence
from typing import NamedTuple

from pydantic import BaseModel

from lms_python.models.source import Room, Student


class IngestionSpec[T: BaseModel](NamedTuple):
    """Declarative specification mapping a domain model to a database target.

    :param table_name: Destination database table name.
    :type table_name: str
    :param columns: Positional column names for the target table.
    :type columns: tuple[str, ...]
    :param row_factory: Callable extracting an ordered sequence of column values from a model.
    :type row_factory: Callable[[T], Sequence[object]]
    """

    table_name: str
    columns: tuple[str, ...]
    row_factory: Callable[[T], Sequence[object]]


ROOM_SPEC = IngestionSpec[Room](
    table_name="rooms",
    columns=("id", "room_name"),
    row_factory=lambda r: (r.id, r.name),
)
"""Ingestion specification mapping Room source payloads to the rooms table."""

STUDENT_SPEC = IngestionSpec[Student](
    table_name="students",
    columns=("id", "full_name", "birthday", "gender", "room_id"),
    row_factory=lambda s: (s.id, s.name, s.birthday, s.sex, s.room),
)
"""Ingestion specification mapping Student source payloads to the students table."""

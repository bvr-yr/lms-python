"""Protocols defining structural contracts for data persistence."""

from collections.abc import Iterable, Sequence
from typing import Protocol


class DataLoader(Protocol):
    """Structural interface specifying bulk data loading capabilities."""

    def load(
        self,
        table_name: str,
        *,
        columns: Sequence[str],
        rows: Iterable[Sequence[object]],
    ) -> None:
        """Stream tabular records into a target table.

        :param table_name: Destination database table name.
        :type table_name: str
        :param columns: (keyword-only) Column names matching the positional order of row values.
        :type columns: Sequence[str]
        :param rows: (keyword-only) Iterable yielding ordered sequences of column values.
        :type rows: Iterable[Sequence[object]]
        """

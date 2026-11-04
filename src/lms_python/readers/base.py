from abc import ABC, abstractmethod
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from pydantic import BaseModel

# T = TypeVar("T", bound=BaseModel)

# from pydantic import TypeAdapter
# ta = TypeAdapter(list[model])
# return ta.validate_python(raw_data)


class BaseReader(ABC):
    def get[T: BaseModel](self, file_path: str | Path, model: type[T]) -> Iterator[T]:
        path = Path(file_path).resolve()
        if not path.is_file():
            raise FileNotFoundError(f"Source file not found at: {path!r}")

        raw_data = self._read(path)

        if not isinstance(raw_data, list):
            error_message = (
                f"Expected top-level JSON array in {path.name!r}, "
                f"got {type(raw_data).__name__!r}"
            )
            raise TypeError(error_message)

        # return (model.model_validate(item) for item in raw_data)
        return map(model.model_validate, raw_data)

    @abstractmethod
    def _read(self, path: Path) -> Any: ...

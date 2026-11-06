import logging
from abc import ABC, abstractmethod
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from lms_python.logger import perf_logger

# T = TypeVar("T", bound=BaseModel)

# from pydantic import TypeAdapter
# ta = TypeAdapter(list[model])
# return ta.validate_python(raw_data)


logger = logging.getLogger(__name__)


class BaseReader(ABC):
    @perf_logger
    def get[T: BaseModel](self, file_path: str | Path, model: type[T]) -> Iterator[T]:
        path = Path(file_path).resolve()
        # if not path.is_file():
        #     raise FileNotFoundError(f"source file not found at: {path}")

        raw_data = self._read(path)
        logger.info("read data from %s", file_path)

        if not isinstance(raw_data, list):
            error_message = (
                f"expected top-level JSON array in {path.name!r}, "
                f"got {type(raw_data).__name__!r}"
            )
            raise TypeError(error_message)

        # return (model.model_validate(item) for item in raw_data)
        return map(model.model_validate, raw_data)

    @abstractmethod
    def _read(self, path: Path) -> Any: ...

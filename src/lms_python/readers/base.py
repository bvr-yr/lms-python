"""Abstract base reader definition."""

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
    """Abstract base class defining the contract for parsing source payloads."""

    @perf_logger
    def get[T: BaseModel](self, file_path: str | Path, model: type[T]) -> Iterator[T]:
        """Read source data and return an iterator of validated Pydantic model instances.

        :param file_path: Path to the target source file.
        :type file_path: str | Path
        :param model: Pydantic model class used for row-level schema validation.
        :type model: type[T]
        :return: Iterator yielding validated model instances lazily.
        :rtype: Iterator[T]
        :raises FileNotFoundError: If file_path does not exist on disk.
        :raises TypeError: If top-level serialized content is not a list.
        :raises pydantic.ValidationError: If any item violates the target model schema.
        """
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
    def _read(self, path: Path) -> Any:
        """Deserialize raw file contents from disk into native Python structures.

        :param path: Resolved absolute path to the target file.
        :type path: Path
        :return: Deserialized raw data structure.
        :rtype: Any
        """

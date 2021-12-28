"""Implementation of the BaseModel."""
from typing import Type, TypeVar

from jsons import dumps, load, dump
from pydantic.dataclasses import dataclass

Self = TypeVar('Self', bound='BaseModel')


@dataclass(frozen=True)
class BaseModel:
    """Base model providing serialization funcitonalities."""

    @classmethod
    def from_json(cls: Type[Self], json_obj: object) -> Self:
        """Convert a JSON object to a Python class."""
        return load(json_obj, cls, strict=True)

    @property
    def json(self) -> object:
        """JSON object representation of the Python class."""
        return dump(
            self,
            cls=self.__class__,
            strip_nulls=True,
            strict=True,
            strip_properties=True
        )

    @property
    def json_string(self) -> str:
        """JSON string representation of the Python class."""
        return dumps(self.json, indent=4)

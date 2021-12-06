from dataclasses import dataclass
from functools import cache
from typing import Type, Final, TypeVar

from jsons import dumps, load, dump

T: Final[TypeVar] = TypeVar('T')


@dataclass(frozen=True, slots=True)
class Model:

    @classmethod
    def from_json(cls: Type[T], json_obj: object) -> T:
        return load(json_obj, cls)

    @property
    @cache
    def json(self) -> object:
        return dump(
            self,
            strip_nulls=True,
            strict=True,
            strip_properties=True
        )

    @property
    @cache
    def json_string(self):
        return dumps(self.json, indent=4)

    def __repr__(self) -> str:
        return self.json_string

    def __str__(self) -> str:
        return self.json_string

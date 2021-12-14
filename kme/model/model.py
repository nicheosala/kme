from dataclasses import dataclass
from typing import Type, TypeVar

from jsons import dumps, load, dump

M = TypeVar('M', bound='Model')


@dataclass(frozen=True)
class Model:

    @classmethod
    def from_json(cls: Type[M], json_obj: object) -> M:
        return load(json_obj, cls, strict=True)

    @property
    def json(self) -> object:
        return dump(
            self,
            strip_nulls=True,
            strict=True,
            strip_properties=True
        )

    @property
    def json_string(self) -> str:
        return dumps(self.json, indent=4)

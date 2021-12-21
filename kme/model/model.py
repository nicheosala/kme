from dataclasses import dataclass
from typing import Type, TypeVar, Final

from jsons import dumps, load, dump

Self = TypeVar('Self', bound='Model')


@dataclass(frozen=True)
class Model:

    @classmethod
    def from_json(cls: Type[Self], json_obj: object) -> Self:
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

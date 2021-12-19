from dataclasses import dataclass
from typing import Type, TypeVar, Final

from jsons import dumps, load, dump

Self = TypeVar('Self', bound='Model')


@dataclass(frozen=True)
class Model:

    @classmethod
    def from_json(cls: Type[Self], json_obj: object) -> Self:
        from_json: Final[Self] = load(json_obj, cls, strict=True)
        return from_json

    @property
    def json(self) -> object:
        json: Final[object] = dump(
            self,
            strip_nulls=True,
            strict=True,
            strip_properties=True
        )
        return json

    @property
    def json_string(self) -> str:
        json_string: Final[str] = dumps(self.json, indent=4)
        return json_string

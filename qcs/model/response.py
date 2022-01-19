from dataclasses import dataclass
from typing import Type, TypeVar

from jsons import dump, dumps, loads

from qcs.configs.configs import Base
from qcs.orm import Block

Self = TypeVar('Self', bound='Response')


@dataclass(frozen=True)
class Response:

    @classmethod
    def from_json(cls: Type[Self], json_str: str) -> Self:
        return loads(json_str, cls, strict=True)

    @property
    def json(self) -> object:
        return dump(
            self,
            strip_nulls=True,
            strict=True,
            strip_properties=True,
            strip_privates=True
        )

    @property
    def json_string(self) -> str:
        return dumps(self.json, indent=4)


@dataclass(frozen=True)
class GetResponse(Response):
    blocks: tuple[Block, ...] = tuple()

    @classmethod
    def from_json(cls: Type[Self], json_str: str) -> Self:
        if Base.COMPATIBILITY_MODE:
            return loads('{ "blocks":' + json_str + '}', cls, strict=True)
        return loads(json_str, cls, strict=True)

    @property
    def json_string(self) -> str:
        if Base.COMPATIBILITY_MODE:
            return dumps(self.blocks, indent=4)
        return dumps(self.json, indent=4)


@dataclass(frozen=True)
class EmptyResponse(Response):
    """A Response that does not cointain anything."""


@dataclass(frozen=True)
class DeleteResponse(Response):
    command: str = "Keys deleted"
    parameter: str = ""
    value: str = "Done"

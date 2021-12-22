from dataclasses import dataclass
from typing import Type, TypeVar, Any

from jsons import dump, dumps, loads, load

from qcs.configs import Config
from qcs.orm import Block

Self = TypeVar('Self', bound='Response')


@dataclass(frozen=True, slots=True)
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
            strip_properties=True
        )

    @property
    def json_string(self) -> str:
        return dumps(self.json, indent=4)


@dataclass(frozen=True, slots=True)
class GetResponse(Response):
    blocks: tuple[Block, ...] = tuple()

    @classmethod
    def from_json(cls: Type[Self], json_str: str) -> Self:
        if Config.COMPATIBILITY_MODE:
            # The received string is not a valid json string. Convert it to
            # valid json.
            return loads('{ "blocks":' + json_str[1:-1] + '}',
                         cls, strict=True)
        return loads(json_str, cls, strict=True)

    @property
    def json_string(self) -> str:
        if Config.COMPATIBILITY_MODE:
            # The produced object is a valid json string. Convert it to an
            # invalid json string.
            blocks = load(self.json, dict[str, Any], strict=True)['blocks']
            return '{' + dumps(blocks, indent=4) + '}'
        return dumps(self.json, indent=4)


@dataclass(frozen=True, slots=True)
class EmptyResponse(Response):
    pass


@dataclass(frozen=True, slots=True)
class DeleteResponse(Response):
    command: str = "Keys deleted"
    parameter: str = ""
    value: str = "Done"

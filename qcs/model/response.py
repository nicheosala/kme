from dataclasses import dataclass
from typing import Final, Type, TypeVar

from jsons import dump, dumps, loads, load

from qcs.configs import Config
from qcs.orm import Block

Self = TypeVar('Self', bound='Response')


@dataclass(frozen=True, slots=True)
class Response:

    @classmethod
    def from_json(cls: Type[Self], json_str: str) -> Self:
        from_json: Final[Self] = loads(json_str, cls, strict=True)
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
        json_string: str = dumps(self.json, indent=4)
        return json_string


@dataclass(frozen=True, slots=True)
class GetResponse(Response):
    blocks: tuple[Block, ...] = tuple()

    @classmethod
    def from_json(cls: Type[Self], json_str: str) -> Self:
        if Config.COMPATIBILITY_MODE:
            # The received string is not a valid json string. Convert it to
            # valid json.
            json_str = '{ "blocks":' + json_str[1:-1] + '}'
        from_json: Final[Self] = loads(json_str, cls, strict=True)
        return from_json

    @property
    def json_string(self) -> str:
        json_string: str = dumps(self.json, indent=4)
        if Config.COMPATIBILITY_MODE:
            # The produced object is a valid json string. Convert it to an
            # invalid json string.
            blocks = load(self.json)['blocks']
            json_string = '{' + dumps(blocks) + '}'
        return json_string


@dataclass(frozen=True, slots=True)
class EmptyResponse(Response):
    pass


@dataclass(frozen=True, slots=True)
class DeleteResponse(Response):
    command: str = "Keys deleted"
    parameter: str = ""
    value: str = "Done"

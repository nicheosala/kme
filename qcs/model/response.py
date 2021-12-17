from dataclasses import dataclass

from qcs.orm import Block


@dataclass(frozen=True, slots=True)
class Response:
    pass


@dataclass(frozen=True, slots=True)
class GetResponse(Response):
    blocks: tuple[Block, ...] = tuple()


@dataclass(frozen=True, slots=True)
class EmptyResponse(Response):
    pass


@dataclass(frozen=True, slots=True)
class DeleteResponse(Response):
    command: str = "Keys deleted"
    parameter: str = ""
    value: str = "Done"

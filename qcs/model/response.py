from dataclasses import dataclass

from .block import Block


@dataclass(frozen=True, slots=True)
class Response:
    blocks: tuple[Block, ...] = tuple()


@dataclass(frozen=True, slots=True)
class EmptyResponse(Response):
    pass

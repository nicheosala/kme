import logging
from dataclasses import dataclass
from uuid import UUID

from jsons import loads

from .command import Command
from ..block import Block
from ..response import Response, EmptyResponse


@dataclass(frozen=True, slots=True)
class GetBlockById(Command):

    def execute(self) -> Response:
        try:
            blocks: list[Block] = []
            for block_id in loads(self.value, tuple[UUID, ...]):
                if block := self.database.blocks.get(block_id):
                    blocks.append(block)
                else:
                    logging.info(f"Block with ID {block_id} not present inside the database, so not found")
            return Response(tuple(blocks))
        except ValueError:
            logging.error("request.value cannot be interpreted as tuple[UUID, ...]")
            return EmptyResponse()  # TODO

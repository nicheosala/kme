import logging
from dataclasses import dataclass
from uuid import UUID

from jsons import loads, DeserializationError

from qcs.orm import Block
from qcs.model import Response, EmptyResponse, GetResponse
from qcs.commands import Command


@dataclass(frozen=True, slots=True)
class GetBlockById(Command):

    def execute(self) -> Response:
        try:
            blocks: list[Block] = []
            for block_id in loads(self.value, tuple[UUID, ...]):
                if block := self.database.blocks.get(block_id):
                    blocks.append(block)
                else:
                    logging.info(
                        f"Block with ID {block_id} not present inside the "
                        f"database, so not found")
            return GetResponse(tuple(blocks))
        except DeserializationError:
            logging.error(
                "request.value cannot be interpreted as tuple[UUID, ...]")
            return EmptyResponse()  # TODO

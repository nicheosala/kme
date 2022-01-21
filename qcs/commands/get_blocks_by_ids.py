import logging
from dataclasses import dataclass
from uuid import UUID

from jsons import loads, DeserializationError

from qcs.commands import Command
from qcs.model import Response, GetResponse, BlockNotFoundResponse, ErrorResponse
from qcs.orm import Block


@dataclass(frozen=True, slots=True)
class GetBlocksByIds(Command):
    def execute(self) -> Response:
        try:
            blocks: list[Block] = []
            for block_id in loads(self.value, tuple[UUID, ...], strict=True):
                if block := self.database.blocks.get(block_id):
                    blocks.append(block)
                else:
                    logging.getLogger("qcs").info(
                        f"Block with ID {block_id} not found into the database"
                    )
                    return BlockNotFoundResponse(
                        details={"not_found_blocks": (block_id,)}
                    )
            return GetResponse(tuple(blocks))
        except DeserializationError:
            logging.getLogger("qcs").error(
                "request.value cannot be interpreted as tuple[UUID, ...]"
            )
            return ErrorResponse("Deserialization error")

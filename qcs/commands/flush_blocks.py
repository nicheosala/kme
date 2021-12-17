import logging
from dataclasses import dataclass

from qcs.model import Response, EmptyResponse
from qcs.commands import Command


@dataclass(frozen=True, slots=True)
class FlushBlocks(Command):

    def execute(self) -> Response:
        self.database.blocks.clear()
        logging.info("All the blocks inside the database have been flushed.")
        return EmptyResponse()  # TODO

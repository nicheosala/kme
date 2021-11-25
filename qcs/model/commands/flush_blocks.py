import logging
from dataclasses import dataclass

from ..commands.command import Command
from ..response import Response, EmptyResponse


@dataclass(frozen=True, slots=True)
class FlushBlocks(Command):

    def execute(self) -> Response:
        self.database.blocks.clear()
        logging.info("All the blocks inside the database have been flushed.")
        return EmptyResponse()  # TODO

import logging
from dataclasses import dataclass

from qcs.commands import Command
from qcs.model import Response, EmptyResponse


@dataclass(frozen=True, slots=True)
class FlushBlocks(Command):
    """Command invoked in order to flush all blocks."""

    def execute(self) -> Response:
        self.database.blocks.clear()
        logging.info("All the blocks inside the database have been flushed.")
        return EmptyResponse()  # TODO

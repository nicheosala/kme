import logging
from dataclasses import dataclass
from uuid import UUID

from jsons import DeserializationError, loads

from ..commands.command import Command
from ..response import Response, EmptyResponse


@dataclass(frozen=True, slots=True)
class DeleteBlocksByIDs(Command):

    def execute(self) -> Response:
        try:
            for block_id in loads(self.value, tuple[UUID, ...]):
                if self.database.blocks.pop(block_id, None):
                    logging.info(f"Block with ID {block_id} deleted")
                else:
                    logging.info(f"Block with ID {block_id} not present inside the database, so not deleted")
        except DeserializationError:
            logging.error(f"Cannot deserialize request value as tuple[UUID, ...]: {self.value}")
        except ValueError:
            logging.error("request.value cannot be interpreted as tuple[UUID, ...]")
        return EmptyResponse()  # TODO this does not respect the specs!

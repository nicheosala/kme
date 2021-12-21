import logging
from dataclasses import dataclass
from uuid import UUID

from jsons import DeserializationError, loads

from qcs.model import Response, EmptyResponse
from qcs.commands import Command


@dataclass(frozen=True, slots=True)
class DeleteBlocksByIDs(Command):

    def execute(self) -> Response:
        try:
            for block_id in loads(self.value, tuple[UUID, ...], strict=True):
                if self.database.blocks.pop(block_id, None):
                    logging.info(f"Block with ID {block_id} deleted")
                else:
                    logging.info(
                        f"Block with ID {block_id} not present inside the "
                        f"database, so not deleted")
        except DeserializationError:
            logging.error(
                f"Cannot deserialize request value as "
                f"tuple[UUID, ...]: {self.value}")
        except ValueError:
            logging.error(
                "request.value cannot be interpreted as tuple[UUID, ...]")
        return EmptyResponse()  # TODO this does not respect the specs!

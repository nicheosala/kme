import logging
from dataclasses import dataclass
from uuid import UUID

from jsons import DeserializationError, loads

from qcs.commands import Command
from qcs.model import Response, EmptyResponse


@dataclass(frozen=True, slots=True)
class DeleteBlocksByIDs(Command):
    def execute(self) -> Response:
        try:
            for block_id in loads(self.value, tuple[UUID, ...], strict=True):
                if self.database.blocks.pop(block_id, None):
                    logging.getLogger("qcs").info(f"Block with ID {block_id} deleted")
                else:
                    logging.getLogger("qcs").info(
                        f"Block with ID {block_id} not present inside the "
                        f"database, so not deleted"
                    )
        except DeserializationError:
            logging.getLogger("qcs").error(
                f"Cannot deserialize request value as "
                f"tuple[UUID, ...]: {self.value}"
            )
        except ValueError:
            logging.getLogger("qcs").error(
                "request.value cannot be interpreted as tuple[UUID, ...]"
            )
        return EmptyResponse()  # TODO this does not respect the specs!

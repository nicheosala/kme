import logging
from dataclasses import dataclass

from qcs.model import Response, EmptyResponse
from qcs.commands import Command


@dataclass(frozen=True, slots=True)
class NotFound(Command):
    """The string received by the client is not recognized as a valid
    command. """

    def execute(self) -> Response:
        logging.info("The string received by the client is not recognized as "
                     "a valid command.")
        return EmptyResponse()

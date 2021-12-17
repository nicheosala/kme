from abc import ABC
from dataclasses import dataclass

from qcs.database import Database
from qcs.model import Response


@dataclass(frozen=True, slots=True)
class Command(ABC):
    """Generic interface of a class managing a command received by a client."""
    value: str
    attribute: str
    database: Database

    def execute(self) -> Response:
        raise NotImplementedError

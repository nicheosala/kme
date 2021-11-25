from abc import abstractmethod, ABC
from dataclasses import dataclass

from ..database import Database
from ..response import Response


@dataclass(frozen=True, slots=True)
class Command(ABC):
    """Generic interface of a class managing a command received by a client."""
    value: str
    attribute: str
    database: Database

    @abstractmethod
    def execute(self) -> Response:
        raise NotImplementedError

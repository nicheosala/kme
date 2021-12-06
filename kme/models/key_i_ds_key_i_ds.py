from dataclasses import dataclass

from .error import EmptyValueError
from .model import Model


@dataclass(frozen=True, slots=True)
class KeyIDsKeyIDs(Model):
    key_ID: str
    key_ID_extension: object | None = None

    def __post_init__(self) -> None:
        if self.key_ID is None:
            raise EmptyValueError

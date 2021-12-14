from dataclasses import dataclass

from kme.errors import EmptyValueError
from kme.model import KeyIDsKeyIDs, Model


@dataclass(frozen=True, slots=True)
class KeyIDs(Model):
    """Key IDs data format is used for a request data model of API "Get key with key IDs" method."""
    key_IDs: tuple[KeyIDsKeyIDs, ...]
    key_IDs_extension: object | None = None

    def __post_init__(self) -> None:
        if self.key_IDs is None:
            raise EmptyValueError

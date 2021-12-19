from dataclasses import dataclass
from uuid import UUID

from kme.errors import EmptyValueError
from kme.model import Model


@dataclass(frozen=True, slots=True)
class KeyIDsKeyIDs(Model):
    key_ID: UUID
    key_ID_extension: object | None = None

    def __post_init__(self) -> None:
        if self.key_ID is None:
            raise EmptyValueError


@dataclass(frozen=True, slots=True)
class KeyIDs(Model):
    """Key IDs data format is used for a request data model of API "Get key
    with key IDs" method. """
    key_IDs: tuple[KeyIDsKeyIDs, ...]
    key_IDs_extension: object | None = None

    def __post_init__(self) -> None:
        if self.key_IDs is None:
            raise EmptyValueError

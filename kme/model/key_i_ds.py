from typing import Optional, Any
from uuid import UUID

from pydantic import BaseModel

from kme.errors import EmptyValueError


class KeyIDsKeyIDs(BaseModel):
    key_ID: UUID
    key_ID_extension: Optional[Any] = None

    def __post_init__(self) -> None:
        if self.key_ID is None:
            raise EmptyValueError


class KeyIDs(BaseModel):
    """Key IDs data format is used for a request data model of API "Get key
    with key IDs" method. """
    key_IDs: tuple[KeyIDsKeyIDs, ...]
    key_IDs_extension: Optional[Any] = None

    def __post_init__(self) -> None:
        if self.key_IDs is None:
            raise EmptyValueError

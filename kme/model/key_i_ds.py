from typing import Optional, Any
from uuid import UUID

from pydantic import BaseModel


class KeyIDsKeyIDs(BaseModel):
    key_ID: UUID
    key_ID_extension: Optional[Any] = None


class KeyIDs(BaseModel):
    """Key IDs data format is used for a request data model of API "Get key
    with key IDs" method. """
    key_IDs: tuple[KeyIDsKeyIDs, ...]
    key_IDs_extension: Optional[Any] = None

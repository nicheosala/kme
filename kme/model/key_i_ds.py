"""Contains the implementation of a KeyIDs object."""
from typing import Optional, Any
from uuid import UUID

from pydantic import BaseModel


class KeyIDsKeyIDs(BaseModel):
    """Object contained in a KeyIDs object."""

    key_ID: UUID
    key_ID_extension: Optional[Any] = None


class KeyIDs(BaseModel):
    """Key IDs is used for a request of API 'Get key with key IDs'."""

    key_IDs: tuple[KeyIDsKeyIDs, ...]
    key_IDs_extension: Optional[Any] = None

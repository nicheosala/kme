"""Contains the implementation of a KeyIDs object."""
from typing import Optional, Any
from uuid import UUID

from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class KeyIDsKeyIDs:
    """Object contained in a KeyIDs object."""

    key_ID: UUID
    key_ID_extension: Optional[Any] = None


@dataclass(frozen=True)
class KeyIDs:
    """Key IDs is used for a request of API 'Get key with key IDs'."""

    key_IDs: tuple[KeyIDsKeyIDs, ...]
    key_IDs_extension: Optional[Any] = None

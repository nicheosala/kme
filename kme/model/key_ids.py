"""Contains the implementation of a KeyIDs object."""
from typing import Optional, Any
from uuid import UUID

from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class KeyIDsKeyIDs:
    """KeyIDsKeyIDs."""

    key_ID: UUID
    key_ID_extension: Optional[Any] = None


@dataclass(frozen=True)
class KeyIDs:
    """KeyIDs.

    Key IDs data format is used for a request data model of API "Get key
    with key IDs" method.
    """

    key_IDs: tuple[KeyIDsKeyIDs, ...]
    key_IDs_extension: Optional[Any] = None

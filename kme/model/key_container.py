"""Contains the implementation of a Key Container object."""
from typing import Optional, Any
from uuid import UUID

from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class Key:
    """Random digital data with an associated universally unique ID."""

    key_ID: UUID
    key: str
    key_ID_extension: Optional[Any] = None
    key_extension: Optional[Any] = None


@dataclass(frozen=True)
class KeyContainer:
    """Key container is used for 'Get key' and 'Get key with key IDs'."""

    keys: tuple[Key, ...]
    key_container_extension: Optional[Any] = None

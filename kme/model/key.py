"""Contains the implementation of a Key object."""
from typing import Any, Optional
from uuid import UUID

from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class Key:
    """Random digital data with an associated universally unique ID."""

    key_ID: UUID
    key: str
    key_ID_extension: Optional[Any] = None
    key_extension: Optional[Any] = None

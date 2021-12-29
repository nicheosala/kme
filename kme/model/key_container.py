"""Contains the implementation of a Key Container object."""
from typing import Optional, Any

from pydantic.dataclasses import dataclass

from kme.model import Key


@dataclass(frozen=True)
class KeyContainer:
    """Key container is used for 'Get key' and 'Get key with key IDs'."""

    keys: tuple[Key, ...]
    key_container_extension: Optional[Any] = None

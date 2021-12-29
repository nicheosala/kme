"""Contains the implementation of a Key Container object."""
from typing import Optional, Any
from uuid import UUID

from pydantic import Field
from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class Key:
    """Random digital data with an associated universally unique ID."""

    key_ID: UUID = Field(
        ...,
        description="""ID of the key"""
    )

    key: str = Field(
        ...,
        description="""
        Key data encoded by base64. The key size is specified by
        the "size" parameter in "Get key". If not specified, the
        "key_size" value in Status data model is used as the default
        size."""
    )

    key_ID_extension: Optional[Any] = Field(
        default=None,
        description="""(Option) for future use."""
    )

    key_extension: Optional[Any] = Field(
        default=None,
        description="""(Option) for future use."""
    )


@dataclass(frozen=True)
class KeyContainer:
    """Key container is used for 'Get key' and 'Get key with key IDs'."""

    keys: tuple[Key, ...] = Field(
        ...,
        description="""
        Array of keys. The number of keys is specified by the
        "number" parameter in "Get key". If not specified, the default
        number of keys is 1."""
    )

    key_container_extension: Optional[Any] = Field(
        default=None,
        description="""(Option) for future use."""
    )

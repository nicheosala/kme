"""The implementation of a Status object."""
from typing import Optional, Any

from pydantic import Field
from pydantic.dataclasses import dataclass

from kme.configs import Config


@dataclass(frozen=True)
class Status:
    """Status.

    Status contains information on keys available to be requested by a
    master SAE for a specified slave SAE.
    """

    source_KME_ID: str = Field(
        ...,
        description="""KME ID of the KME"""
    )

    target_KME_ID: str = Field(
        ...,
        description="""KME ID of the target KME"""
    )

    master_SAE_ID: str = Field(
        ...,
        description="""SAE ID of the calling master SAE"""
    )

    slave_SAE_ID: str = Field(
        ...,
        description="""SAE ID of the specified slave SAE"""
    )

    key_size: int = Field(
        default=Config.DEFAULT_KEY_SIZE,
        description="""
        Default size of key the KME can deliver to the SAE (in bit)"""
    )

    stored_key_count: int = Field(
        default=Config.STORED_KEY_COUNT,
        description="""Number of stored keys KME can deliver to the SAE"""
    )

    max_key_count: int = Field(
        default=Config.MAX_KEY_COUNT,
        description="""Maximum number of stored_key_count"""
    )

    max_key_per_request: int = Field(
        default=Config.MAX_KEY_PER_REQUEST,
        description="""Maximum number of keys per request"""
    )

    max_key_size: int = Field(
        default=Config.MAX_KEY_SIZE,
        description="""
        Maximum size of key the KME can deliver to the SAE (in bit)"""
    )

    min_key_size: int = Field(
        default=Config.MIN_KEY_SIZE,
        description="""
        Minimum size of key the KME can deliver to the SAE (in bit)"""
    )

    max_SAE_ID_count: int = Field(
        default=Config.MAX_SAE_ID_COUNT,
        description="""
        Maximum number of additional_slave_SAE_IDs the KME allows. "0" when
        the KME does not support key multicast
        """
    )

    status_extension: Optional[Any] = Field(
        default=None,
        description="""(Option) for future use"""
    )

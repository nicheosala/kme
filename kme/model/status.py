"""Contains the implementation of a Status object."""
from typing import Optional, Any

from pydantic.dataclasses import dataclass

from kme.model import BaseModel


@dataclass(frozen=True)
class Status(BaseModel):
    """A status object.

    Status contains information on keys available to be requested by a
    master SAE for a specified slave SAE.
    """

    source_KME_ID: str
    """KME ID of the KME"""

    target_KME_ID: str
    """KME ID of the target KME"""

    master_SAE_ID: str
    """SAE ID of the calling master SAE"""

    slave_SAE_ID: str
    """SAE ID of the specified slave SAE"""

    key_size: int
    """Default size of key the KME can deliver to the SAE (in bit)"""

    stored_key_count: int
    """Number of stored keys KME can deliver to the SAE"""

    max_key_count: int
    """Maximum number of stored_key_count"""

    max_key_per_request: int
    """Maximum number of keys per request"""

    max_key_size: int
    """Maximum size of key the KME can deliver to the SAE (in bit)"""

    min_key_size: int
    """Minimum size of key the KME can deliver to the SAE (in bit)"""

    max_SAE_ID_count: int
    """
    Maximum number of additional_slave_SAE_IDs the KME allows. "0" when
    the KME does not support key multicast
    """

    status_extension: Optional[Any] = None
    """(Option) for future use"""

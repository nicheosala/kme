from typing import Optional, Any

from pydantic import BaseModel


class Status(BaseModel):
    """Status contains information on keys available to be requested by a
    master SAE for a specified slave SAE. """
    source_KME_ID: str
    target_KME_ID: str
    master_SAE_ID: str
    slave_SAE_ID: str
    key_size: int
    stored_key_count: int
    max_key_count: int
    max_key_per_request: int
    max_key_size: int
    min_key_size: int
    max_SAE_ID_count: int
    status_extension: Optional[Any] = None

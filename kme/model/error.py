from typing import Optional, Any

from pydantic import BaseModel


class Error(BaseModel):
    """Generic Error defined respecting standard ETSI GS QKD 014."""
    message: str
    details: Optional[tuple[dict[str, Any], ...]] = None

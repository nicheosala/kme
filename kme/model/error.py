from typing import Optional, Any

from pydantic import BaseModel


class Error(BaseModel):
    """Generic Error defined respecting standard ETSI GS QKD 014."""
    message: str
    details: Optional[tuple[dict[str, Any], ...]] = None


class ServiceUnavailable(Error):  # status code 503
    pass


class BadRequest(Error):  # Status code 400
    pass


class Unauthorized(Error):  # Status code 401
    pass

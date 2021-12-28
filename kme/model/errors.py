"""Contains the definition of errors that may be raised by kme."""
from typing import Optional, Any

from pydantic.dataclasses import dataclass

from kme.model import BaseModel


@dataclass(frozen=True)
class Error(BaseModel):
    """Generic Error defined respecting standard ETSI GS QKD 014."""

    message: str
    details: Optional[tuple[dict[str, Any], ...]] = None


@dataclass(frozen=True)
class ServiceUnavailable(Error):
    """Exception with status code 503."""

    pass


@dataclass(frozen=True)
class BadRequest(Error):
    """Exception with status code 400."""

    pass


@dataclass(frozen=True)
class Unauthorized(Error):
    """Exception with status code 401."""

    pass

"""Contains the implementation of an Error object."""
from typing import Any

from fastapi import HTTPException
from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class Error:
    """Generic Error defined respecting standard ETSI GS QKD 014."""

    message: str

    details: tuple[dict[str, Any], ...] | None = None
    """(Option) Array to supply additional detailed error 
    information specified as name/value pairs. Values may be of any 
    type, including objects. """


@dataclass(frozen=True)
class ServiceUnavailable(Error):
    """Error with status code 503."""


@dataclass(frozen=True)
class BadRequest(Error):
    """Error with status code 400."""


@dataclass(frozen=True)
class Unauthorized(Error):
    """Error with status code 401."""


@dataclass(frozen=True)
class KeyNotFound(HTTPException):
    """Error when a requested key is not found."""

    detail: str = "One or more keys specified are not found on KME"
    status_code: int = 400

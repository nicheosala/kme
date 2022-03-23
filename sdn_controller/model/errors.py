"""Contains the implementation of an Error object."""
from typing import Any

from fastapi import HTTPException
from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class Error:
    # TODO check
    """Generic Error defined respecting standard ETSI GS QKD 015."""

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
class KmeNotFound(HTTPException):
    # TODO check
    """Error when a requested key is not found."""

    detail: str = "The KME specified has not been found."
    status_code: int = 400


@dataclass(frozen=True)
class SaeNotFound(HTTPException):
    # TODO check
    """Error when a requested SAE is not found."""

    detail: str = "The SAE specified has not been found."
    status_code: int = 400

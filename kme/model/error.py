from typing import Optional, Any

from pydantic import BaseModel

from kme.errors import EmptyValueError


class Error(BaseModel):
    """Generic Error defined respecting standard ETSI GS QKD 014."""
    message: str
    details: Optional[tuple[dict[str, Any], ...]] = None

    def __post_init__(self) -> None:
        if self.message is None:
            raise EmptyValueError

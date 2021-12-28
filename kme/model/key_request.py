"""Contains the implementation of a Key Request object."""
from typing import Any

from pydantic.dataclasses import dataclass

from kme.configs import Config
from kme.model import BaseModel


@dataclass(frozen=True)
class KeyRequest(BaseModel):
    """Key request is used for a request data model of API 'Get key' method."""

    number: int = 1
    size: int = Config.DEFAULT_KEY_SIZE
    additional_slave_SAE_IDs: tuple[str, ...] = tuple()
    extension_mandatory: tuple[dict[str, Any], ...] = tuple()
    extension_optional: tuple[dict[str, Any], ...] = tuple()

    @property
    def supported_extension_parameters(self) -> frozenset[str]:
        """Add supported extension parameters here."""
        return frozenset()

"""Contains the implementation of a Key Request object."""
from dataclasses import dataclass
from typing import Any

from kme.configs import Config


@dataclass
class KeyRequest:
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

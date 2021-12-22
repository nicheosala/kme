from typing import Any

from pydantic import BaseModel


class KeyRequest(BaseModel):
    """Key request data format is used for a request data model of API "Get
    key" method. """
    number: int = 1
    # TODO "default value is defined as key_size in Status data format"
    size: int = 64
    additional_slave_SAE_IDs: tuple[str, ...] = tuple()
    extension_mandatory: tuple[dict[str, Any], ...] = tuple()
    extension_optional: tuple[dict[str, Any], ...] = tuple()

    @property
    def supported_extension_parameters(self) -> frozenset[str]:
        """Add supported extension parameters here."""
        return frozenset()

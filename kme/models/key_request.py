from dataclasses import dataclass
from functools import cache
from typing import Any

from immutabledict import immutabledict

from .model import Model


@dataclass(frozen=True, slots=True)
class KeyRequest(Model):
    """Key request data format is used for a request data model of API "Get key" method."""
    number: int = 1
    size: int = 8  # TODO "default value is defined as key_size in Status data format"
    additional_slave_SAE_IDs: tuple[str, ...] | None = None
    extension_mandatory: tuple[immutabledict[str, Any], ...] | None = None
    extension_optional: tuple[immutabledict[str, Any], ...] | None = None

    @property
    @cache
    def supported_extension_parameters(self) -> frozenset:
        """Add supported extension parameters here."""
        return frozenset()

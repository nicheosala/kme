from dataclasses import dataclass
from functools import cache
from typing import Any

from immutabledict import immutabledict

from .model import Model


@dataclass(frozen=True, slots=True)
class KeyRequest(Model):
    """Key request data format is used for a request data model of API "Get key" method."""
    number: int = 1
    size: int = 64  # TODO "default value is defined as key_size in Status data format"
    additional_slave_SAE_IDs: tuple[str, ...] = tuple()
    extension_mandatory: tuple[immutabledict[str, Any], ...] = tuple()
    extension_optional: tuple[immutabledict[str, Any], ...] = tuple()

    @property
    @cache
    def supported_extension_parameters(self) -> frozenset[str]:
        """Add supported extension parameters here."""
        return frozenset()

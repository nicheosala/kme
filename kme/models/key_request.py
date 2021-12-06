from dataclasses import dataclass

from .base_model_ import Model


@dataclass(frozen=True, slots=True)
class KeyRequest(Model):
    """Key request data format is used for a request data model of API "Get key" method."""
    number: int = 1
    size: int = 1  # TODO "default value is defined as key_size in Status data format"
    additional_slave_SAE_IDs: tuple[str, ...] | None = None
    extension_mandatory: tuple[object, ...] | None = None
    extension_optional: tuple[object, ...] | None = None

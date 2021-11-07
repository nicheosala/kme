from dataclasses import dataclass

from .base_model_ import Model


@dataclass(frozen=True)
class KeyRequest(Model):
    number: int | None = 1
    size: int | None = 1  # TODO "default value is defined as key_size in Status data format"
    additional_slave_SAE_IDs: list[str] | None = None
    extension_mandatory: list[object] | None = None
    extension_optional: list[object] | None = None

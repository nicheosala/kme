from dataclasses import dataclass
from typing import Optional
from KME.models.base_model_ import Model


@dataclass(frozen=True)
class KeyRequest(Model):
    number: Optional[int] = 1
    size: Optional[int] = 1     # TODO "default value is defined as key_size in Status data format"
    additional_slave_SAE_IDs: Optional[list[str]] = None
    extension_mandatory: Optional[list[object]] = None
    extension_optional: Optional[list[object]] = None

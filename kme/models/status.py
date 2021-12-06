from dataclasses import dataclass

from .error import EmptyValueError
from .model import Model


@dataclass(frozen=True, slots=True)
class Status(Model):
    """Status contains information on keys available to be requested by a master SAE for a specified slave SAE."""
    source_KME_ID: str
    target_KME_ID: str
    master_SAE_ID: str
    slave_SAE_ID: str
    key_size: int
    stored_key_count: int
    max_key_count: int
    max_key_per_request: int
    max_key_size: int
    min_key_size: int
    max_SAE_ID_count: int
    status_extension: object | None = None

    def __post_init__(self) -> None:
        if (
                self.source_KME_ID is None or
                self.target_KME_ID is None or
                self.master_SAE_ID is None or
                self.slave_SAE_ID is None or
                self.key_size is None or
                self.stored_key_count is None or
                self.max_key_count is None or
                self.max_key_per_request is None or
                self.max_key_size is None or
                self.min_key_size is None or
                self.max_SAE_ID_count is None
        ):
            raise EmptyValueError

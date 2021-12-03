from dataclasses import dataclass

from kme.models.base_model_ import Model


@dataclass(frozen=True, slots=True)
class EmptyValueError(Exception):
    """Error thrown when attempting to set to None a value that cannot be null."""

    def __str__(self) -> str:
        return f"Non nullable field set to `None`"


@dataclass(frozen=True, slots=True)
class Error(Model):
    """Generic Error defined respecting standard ETSI GS QKD 014."""
    message: str
    details: list[object] | None = None

    def __post_init__(self) -> None:
        if self.message is None:
            raise EmptyValueError

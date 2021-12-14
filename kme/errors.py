from dataclasses import dataclass
from typing import Any

from immutabledict import immutabledict

from kme.model import Model


@dataclass(frozen=True, slots=True)
class Error(Model, Exception):
    """Generic Error defined respecting standard ETSI GS QKD 014."""
    message: str
    details: tuple[immutabledict[str, Any], ...] | None = None
    status: int = 503

    def __post_init__(self) -> None:
        if self.message is None:
            raise EmptyValueError

    @property
    def json(self) -> object:
        d: dict[str, Any] = {'message': self.message}
        if self.details:
            d.update({'details': self.details})
        return d


@dataclass(frozen=True, slots=True)
class EmptyValueError(Error):
    message: str = "Non nullable field set to `None`"


@dataclass(frozen=True, slots=True)
class KeyNotFoundError(Error):
    message: str = "One or more keys specified are not found on KME"
    status: int = 400


@dataclass(frozen=True, slots=True)
class UnsupportedMandatoryExtensionParameterError(Error):
    message: str = "Not all 'extension_mandatory' parameters are supported"
    status: int = 400


@dataclass(frozen=True, slots=True)
class UnmetMandatoryExtensionParameterError(Error):
    message: str = "Not all 'extension_mandatory' request options could be met"
    status: int = 400


@dataclass(frozen=True, slots=True)
class SizeNotMultipleOfEightError(Error):
    message: str = "Requested key size shall be a multiple of 8"
    status: int = 400

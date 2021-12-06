from dataclasses import dataclass
from functools import cache

from kme.models.base_model_ import Model


@dataclass(frozen=True, slots=True)
class Error(Model, Exception):
    """Generic Error defined respecting standard ETSI GS QKD 014."""
    message: str
    details: tuple[object, ...] | None = None
    status: int = 503

    def __post_init__(self) -> None:
        if self.message is None:
            raise EmptyValueError

    @property
    @cache
    def json(self) -> object:
        d: dict = {'message': self.message}
        if self.details:
            d.update({'details': self.details})
        return d


@dataclass(frozen=True, slots=True)
class EmptyValueError(Error):
    message: str = "Non nullable field set to `None`"


@dataclass(frozen=True, slots=True)
class KeyNotFoundError(Error):
    message: str = "One or more keys specified are not found on kme"
    status: int = 404


@dataclass(frozen=True, slots=True)
class ExtensionMandatoryNotEmptyError(Error):
    """
    Standard ETSI 014 force to manage the content of parameter 'extension_mandatory'.
    So far, this implementation is not able to manage 'extension_mandatory', so it throws the following error.
    """
    message: str = "Field 'extension_mandatory' is not empty and the server shall handle it, but it is not able to " \
                   "do it. "

from fastapi import HTTPException
from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class EmptyValueError(HTTPException):
    detail: str = "Non nullable field set to `None`"
    status_code: int = 400


@dataclass(frozen=True)
class KeyNotFoundError(HTTPException):
    detail: str = "One or more keys specified are not found on KME"
    status_code: int = 400


@dataclass(frozen=True)
class UnsupportedExtensionError(HTTPException):
    detail: str = "Not all 'extension_mandatory' parameters are supported"
    status_code: int = 400


@dataclass(frozen=True)
class UnmetMandatoryExtensionParameterError(HTTPException):
    detail: str = "Not all 'extension_mandatory' request options could be met"
    status_code: int = 400


@dataclass(frozen=True)
class SizeNotMultipleOfEightError(HTTPException):
    detail: str = "Requested key size shall be a multiple of 8"
    status_code: int = 400

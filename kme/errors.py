from dataclasses import dataclass

from fastapi import HTTPException


@dataclass
class EmptyValueError(HTTPException):
    detail: str = "Non nullable field set to `None`"
    status_code: int = 400


@dataclass
class KeyNotFoundError(HTTPException):
    detail: str = "One or more keys specified are not found on KME"
    status_code: int = 400


@dataclass
class UnsupportedExtensionError(HTTPException):
    detail: str = "Not all 'extension_mandatory' parameters are supported"
    status_code: int = 400


@dataclass
class UnmetMandatoryExtensionParameterError(HTTPException):
    detail: str = "Not all 'extension_mandatory' request options could be met"
    status_code: int = 400


@dataclass
class SizeNotMultipleOfEightError(HTTPException):
    detail: str = "Requested key size shall be a multiple of 8"
    status_code: int = 400

"""The implementation of a Key Request object."""
from typing import Any

from pydantic import Field, validator
from pydantic.dataclasses import dataclass

from kme.configs import Config


@dataclass(frozen=True)
class KeyRequest:
    """Key request.

    Key request is used for a request data model of API 'Get key' method.
    """

    number: int = Field(
        default=1,
        description="""
        Number of keys requested, default value is 1.
        """,
        ge=0,
    )

    size: int = Field(
        default=Config.DEFAULT_KEY_SIZE,
        description="""
        Size of each key in bits, default value is defined as key_size in 
        Status data format.
        """,
        multiple_of=8,
        ge=0,
    )

    additional_slave_SAE_IDs: tuple[str, ...] = Field(
        default_factory=tuple,
        description="""
        (Option) Array of IDs of slave SAEs. It is used for specifying 
        two or more slave SAEs to share identical keys. The maximum number 
        of IDs is defined as max_SAE_ID_count in Status data format.
        """,
        min_length=0,
        max_length=Config.MAX_SAE_ID_COUNT,
    )

    extension_mandatory: tuple[dict[str, Any], ...] = Field(
        default_factory=tuple,
        description="""
        (Option) Array of extension parameters specified as name/value 
        pairsthat KME shall handle or return an error. Parameter values may 
        be of any type, including objects.
        """,
    )

    extension_optional: tuple[dict[str, Any], ...] = Field(
        default_factory=tuple,
        description="""
        (Option) Array of extension parameters specified as name/value 
        pairsthat KME may ignore. Parameter values may be of any type, 
        including objects.
        """,
    )

    @validator("extension_mandatory", each_item=True)
    def check_supported_extension_mandatory(cls: Any, ext: dict[str, Any]) -> None:
        """Ensure all mendatory extensions provided are supported."""
        for ext_name in ext.keys():
            if ext_name not in Config.SUPPORTED_EXTENSION_PARAMS:
                raise ValueError("Unsupported mandatory exception")

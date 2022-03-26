from uuid import UUID
from pydantic.dataclasses import dataclass
from pydantic import Field


@dataclass(frozen=True)
class NewAppRequest:
    """New app registration request.
    It is used for a request data model of API 'new_app' method.
    """
    src_flag: bool
    src: UUID
    dst: UUID
    kme: UUID
    qos: dict[str, int | bool] = Field(
        default_factory=dict,
        description="""
        The QoS requested by the SAEs.
        """
    )


@dataclass(frozen=True)
class WaitingForApp:
    """Response to 'new_app' when the other SAE is not registered yet."""
    wait: bool = True


@dataclass(frozen=True)
class RegisterApp:
    """Response to 'new_app' when the two SAEs have been registered"""
    ksid: UUID
    src: UUID
    dst: UUID
    kme_src: UUID
    kme_dst: UUID
    qos: dict[str, int | bool] = Field(
        default_factory=dict,
        description="""
            The QoS requested by the SAEs.
            """
    )

from uuid import UUID
from pydantic.dataclasses import dataclass
from pydantic import Field


@dataclass(frozen=False)
class OpenSessionRequest:
    """Open session request.
    It is used for a request data model of API 'Open key session' method.
    """
    src_flag: bool
    src: UUID
    dst: UUID
    qos: dict[str, int | bool] = Field(
        default_factory=dict,
        description="""
        The QoS requested by the SAEs.
        """
    )


@dataclass(frozen=True)
class OpenSessionResponse:
    """Response to open_key_session with another app."""
    waiting: bool
    ksid: UUID | None

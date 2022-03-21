from uuid import UUID
from pydantic.dataclasses import dataclass
from pydantic import Field


@dataclass(frozen=False)
class OpenSessionRequest:
    """Open session request.

    It is used for a request data model of API 'Open key session' method.
    """

    src: UUID
    dst: UUID
    qos: dict[str, int | bool] = Field(
        default_factory=dict,
        description="""
        The QoS requested by the sae.
        """
    )

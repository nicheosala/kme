from uuid import UUID
from pydantic.dataclasses import dataclass
from pydantic import Field


@dataclass(frozen=False)
class NewAppRequest:
    """New app registration request.

    It is used for a request data model of API 'New app' method.
    """

    src: UUID
    dst: UUID
    kme: UUID
    qos: dict[str, int | bool] = Field(
        default_factory=dict,
        description="""
        The QoS requested by the sae.
        """
    )


@dataclass(frozen=True)
class NewAppResponse:
    """Response to 'new_app'. If the other app is already registered, the Controller will return an assigned
    'key_stream_id', otherwise it will be the Nil UUID.
    """
    sae1: UUID  # TODO useless for now
    sae2: UUID  # TODO useless for now
    key_stream_id: UUID = UUID('00000000-0000-0000-0000-000000000000')

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
    kme: str    # TODO should be a UUID
    qos: dict[str, int | bool] = Field(
        default_factory=dict,
        description="""
        The QoS requested by the sae.
        """
    )

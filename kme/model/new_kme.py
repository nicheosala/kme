from uuid import UUID
from pydantic.dataclasses import dataclass
from pydantic import Field


@dataclass(frozen=False)
class NewKmeRequest:
    """New KME request.

    It is used for a request data model of API 'new_kme' method.
    """

    ip: str
    port: int


@dataclass(frozen=False)
class NewKmeResponse:
    """Response to 'new_kme'.
    """
    kme_id: UUID

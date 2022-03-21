from uuid import UUID

from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class NewAppResponse:
    """Response to 'new_app'. If the other app is already registered, the Controller will return an assigned
    'key_stream_id', otherwise it will be None.
    """
    key_stream_id: UUID = None

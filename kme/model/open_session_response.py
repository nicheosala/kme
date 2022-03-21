from uuid import UUID

from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class OpenSessionResponse:
    """Response to open_key_session with another app.
    If the other app is already registered, the kme will return an assigned 'key_stream_id', otherwise it will be None.
    """
    key_stream_id: UUID = None

import uuid
from typing import Final
from uuid import UUID

from fastapi import APIRouter

from sdn_controller.model.new_app_request import NewAppRequest
from sdn_controller.model.new_app_response import NewAppResponse

router: Final[APIRouter] = APIRouter(tags=["new_app"])


@router.post(
    path="/new_app",
    summary="Register a new app",
    response_model=NewAppResponse,
    response_model_exclude_none=True,
)
async def new_app(
        request: NewAppRequest
) -> NewAppResponse:
    """
    Checks if the 'dst' app in the request is already registered: if so then assigns a uuid to the connection,
    otherwise returns None
    """

    # TODO must check if the dst app is already registered or not
    connection_id = NewAppResponse(key_stream_id=uuid.uuid4())

    return connection_id

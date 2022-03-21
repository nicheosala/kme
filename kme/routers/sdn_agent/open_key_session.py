import uuid
from typing import Final

from httpx import Response, AsyncClient

from kme.configs import Config
from kme.encoder import dump
from kme.model import OpenSessionResponse

from fastapi import APIRouter

from kme.model.open_session_request import OpenSessionRequest
from kme.tests.examples import qos
from sdn_controller import app
from sdn_controller.model.new_app_request import NewAppRequest
from sdn_controller.model.new_app_response import NewAppResponse

router: Final[APIRouter] = APIRouter(tags=["open_key_session"])


@router.post(
    path="/open_key_session",
    summary="Open session with another app",
    response_model=OpenSessionResponse,
    response_model_exclude_none=True,
)
async def open_key_session(
        request: OpenSessionRequest
) -> OpenSessionResponse:
    """
    Forwards the request to the SDN controller with new_app(src, dst, qos, kme_id).
    Then depending on the SDN controller's response, it forwards back to the app a KSID or nothing.
    """

    app_registration: Final[NewAppRequest] = NewAppRequest(
        src=uuid.uuid4(),
        dst=uuid.uuid4(),
        kme=Config.KME_ID,
        qos=qos
    )

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            url=f"/new_app",
            json=dump(app_registration)
        )
        new_app_response: Final[NewAppResponse] = NewAppResponse(**response.json())
        return OpenSessionResponse(key_stream_id=new_app_response.key_stream_id)

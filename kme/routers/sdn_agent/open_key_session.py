from typing import Final

from httpx import AsyncClient

from kme.configs import Config
from kme.encoder import dump

from fastapi import APIRouter

from kme.model.open_session import OpenSessionRequest, OpenSessionResponse
from sdn_controller import sdn_app
from sdn_controller.model.new_app import NewAppRequest

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
        src=request.src, dst=request.dst, kme=Config.KME_ID, qos=request.qos
    )

    async with AsyncClient(app=sdn_app.app, base_url=Config.SDN_CONTROLLER_ADDRESS) as client:
        response = await client.post(
            url=f"/new_app",
            json=dump(app_registration)
        )
        return OpenSessionResponse(**response.json())

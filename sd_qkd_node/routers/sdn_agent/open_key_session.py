from typing import Final

from httpx import AsyncClient

from sd_qkd_node.configs import Config
from sd_qkd_node.encoder import dump

from fastapi import APIRouter

from sd_qkd_node.model.open_session import OpenSessionRequest
from sdn_controller.model.new_app import NewAppRequest

router: Final[APIRouter] = APIRouter(tags=["open_key_session"])


@router.post(
    path="/open_key_session",
    summary="Open session with another app",
    response_model_exclude_none=True,
)
async def open_key_session(
        request: OpenSessionRequest
) -> None:
    """
    Forwards the request to the SDN controller with new_app(src, dst, qos, kme_id).
    Then depending on the SDN controller's response, it forwards back to the app a KSID or nothing.
    """

    app_registration: Final[NewAppRequest] = NewAppRequest(
        src_flag=request.src_flag, src=request.src, dst=request.dst, kme=Config.KME_ID, qos=request.qos
    )

    async with AsyncClient() as client:
        await client.post(
            url=f"{Config.SDN_CONTROLLER_ADDRESS}/new_app",
            json=dump(app_registration)
        )

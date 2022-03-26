from typing import Final

from fastapi import APIRouter
from httpx import AsyncClient

from sd_qkd_node import kme_app
from sdn_controller.database.dbms import find_peer, get_kme_address
from sdn_controller.encoder import dump
from sdn_controller.model.new_app import NewAppRequest, WaitingForApp

router: Final[APIRouter] = APIRouter(tags=["new_app"])


@router.post(
    path="/new_app",
    summary="Register a new app",
    response_model_exclude_none=True,
)
async def new_app(
        request: NewAppRequest
) -> None:
    """
    To register a new connection between two SAEs.
    """
    response = await find_peer(request)
    if isinstance(response, WaitingForApp):
        kme_addr = await get_kme_address(request.kme)
        async with AsyncClient(app=kme_app.app, base_url=kme_addr) as client:
            await client.post(
                url=f"/assign_ksid",
                json=dump(response)
            )
    else:
        kme_src_addr = await get_kme_address(response.kme_src)
        kme_dst_addr = await get_kme_address(response.kme_dst)
        async with AsyncClient() as client:
            await client.post(
                url=f"{kme_src_addr}/assign_ksid",
                json=dump(response)
            )
        async with AsyncClient() as client:
            await client.post(
                url=f"{kme_dst_addr}/assign_ksid",
                json=dump(response)
            )

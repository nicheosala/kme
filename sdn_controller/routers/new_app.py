import uuid
from typing import Final

from fastapi import APIRouter
from httpx import AsyncClient

from kme import kme_app
from kme.model.open_session import OpenSessionResponse
from sdn_controller.database.dbms import add_new_app, get_kme_address
from sdn_controller.encoder import dump
from sdn_controller.model.new_app import NewAppRequest, NewAppResponse

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
    otherwise returns a None Ksid
    """

    connection_id: Final[NewAppResponse] = await add_new_app(request)
    if connection_id.key_stream_id != uuid.UUID('00000000-0000-0000-0000-000000000000'):
        kme_addr: Final[str] = await get_kme_address(request.dst)
        back: Final[OpenSessionResponse] = OpenSessionResponse(
            key_stream_id=connection_id.key_stream_id, sae1=request.dst, sae2=request.src
        )
        async with AsyncClient(app=kme_app.app, base_url=kme_addr) as client:
            await client.post(url=f"/assign_ksid", json=dump(back))
            pass

    return connection_id

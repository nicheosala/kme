from typing import Final

from fastapi import APIRouter

from sdn_controller.database.dbms import add_new_kme
from sd_qkd_node.model.new_kme import NewKmeRequest, NewKmeResponse

router: Final[APIRouter] = APIRouter(tags=["new_kme"])


@router.post(
    path="/new_kme",
    summary="Register a new KME",
    response_model=NewKmeResponse,
    response_model_exclude_none=True,
)
async def new_kme(
        request: NewKmeRequest
) -> NewKmeResponse:
    """
    Adds a new KME in the network seen by the SDN Controller.
    """
    kme: Final[NewKmeResponse] = await add_new_kme(request)

    return kme

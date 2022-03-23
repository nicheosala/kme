from typing import Final

from fastapi import APIRouter

from kme.model.open_session import OpenSessionResponse

router: Final[APIRouter] = APIRouter(tags=["assign_ksid"])


@router.post(
    path="/assign_ksid",
    include_in_schema=False,
)
async def assign_ksid(
        request: OpenSessionResponse
) -> None:
    """
    The SDN Controller calls this API to assign a Ksid to a SAE which was waiting for the other SAE to connect.
    """

    print(f"ksid: {request.key_stream_id} assigned to: {request.sae1} - {request.sae2}")

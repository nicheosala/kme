from typing import Final

from fastapi import APIRouter

from kme.model.open_session import OpenSessionResponse, OpenSessionRequest

router: Final[APIRouter] = APIRouter(tags=["get_ksid"])


@router.post(
    path="/get_ksid",
    include_in_schema=True,
)
async def get_ksid(
        request: OpenSessionRequest
) -> OpenSessionResponse:
    """
    Debugging purposes.
    The SAE asks for the assigned ksid for its connection with another SAE.
    """

    print(f"ksid: {request.key_stream_id} assigned to: {request.sae1} - {request.sae2}")

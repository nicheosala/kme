from typing import Final
from urllib.parse import unquote as url_decode

from fastapi import APIRouter, Path

from kme.model import Status

router: Final[APIRouter] = APIRouter(
    tags=["status"]
)


@router.get(
    path="/api/v1/keys/{slave_SAE_ID}/status",
    summary="Get status",
    response_model=Status,
    response_model_exclude_unset=True
)
async def get_status(
        slave_SAE_ID: str = Path(
            ...,
            description="URL-encoded SAE ID of slave SAE"
        )
) -> Status:
    """
    Returns Status from a kme to the calling SAE
    """
    return Status(
        source_KME_ID="TODO",
        target_KME_ID="TODO",
        master_SAE_ID="TODO",
        slave_SAE_ID=url_decode(slave_SAE_ID),
        key_size=64,
        stored_key_count=-1,
        max_key_count=-1,
        max_key_per_request=-1,
        max_key_size=-1,
        min_key_size=-1,
        max_SAE_ID_count=-1
    )
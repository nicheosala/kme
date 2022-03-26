from typing import Final
from urllib.parse import unquote as url_decode

from fastapi import APIRouter, Path

from sd_qkd_node.model import Status

router: Final[APIRouter] = APIRouter(tags=["status"])


@router.get(
    path="/{slave_SAE_ID}/status",
    summary="Get status",
    response_model=Status,
    response_model_exclude_none=True,
)
async def get_status(
    slave_sae_id: str = Path(..., description="URL-encoded SAE ID of slave SAE")
) -> Status:
    """
    Returns Status from a sd_qkd_node to the calling SAE
    """
    return Status(
        source_KME_ID="TODO",
        target_KME_ID="TODO",
        master_SAE_ID="TODO",
        slave_SAE_ID=url_decode(slave_sae_id),
    )

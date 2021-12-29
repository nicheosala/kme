from typing import Final
from urllib.parse import unquote as url_decode
from uuid import UUID

from fastapi import APIRouter, Query, Path

from kme.database.db import get
from kme.model import KeyContainer, KeyIDs, Key

router: Final[APIRouter] = APIRouter(
    tags=["dec_keys"]
)


@router.get(
    path="/{master_SAE_ID}/dec_keys",
    summary="Get key with key IDs",
    response_model=KeyContainer,
    response_model_exclude_none=True
)
async def get_key_with_key_i_ds(
        master_SAE_ID: str = Path(
            ...,
            description="URL-encoded SAE ID of master SAE"
        ),
        key_ID: UUID = Query(
            ...,
            description="single key ID"
        ),
) -> KeyContainer:
    """
    Returns Key container from the kme to the calling slave SAE. Key
    container contains keys matching those previously delivered to a
    remote master SAE based on the Key IDs supplied from the remote
    master SAE in response to its call to Get key. The kme shall reject
    the request with a 401 HTTP status code if the SAE ID of the
    requester was not an SAE ID supplied to the 'Get key' method each
    time it was called resulting in the return of the Key IDs being
    requested.
    """
    keys: Final[tuple[Key, ...]] = await get(
        key_ID,
        url_decode(master_SAE_ID)
    ),

    return KeyContainer(keys=keys)


@router.post(
    path="/{master_SAE_ID}/dec_keys",
    summary="Post key with key IDs",
    response_model=KeyContainer,
    response_model_exclude_none=True
)
async def post_key_with_key_i_ds(
        key_ids: KeyIDs,
        master_SAE_ID: str = Path(
            ...,
            description="URL-encoded SAE ID of master SAE"
        ),
) -> KeyContainer:
    """
    Returns Key container from the kme to the calling slave SAE. Key
    container contains keys matching those previously delivered to a
    remote master SAE based on the Key IDs supplied from the remote
    master SAE in response to its call to Get key. The kme shall reject
    the request with a 401 HTTP status code if the SAE ID of the
    requester was not an SAE ID supplied to the 'Get key' method each
    time it was called resulting in the return of the Key IDs being
    requested.
    """
    keys: Final[list[Key]] = []
    for key_id in key_ids.key_IDs:
        key: Key = await get(
            key_id.key_ID,
            url_decode(master_SAE_ID)
        )
        keys.append(key)

    return KeyContainer(keys=tuple(keys))

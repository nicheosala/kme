from typing import Final
from urllib.parse import unquote as url_decode

from fastapi import APIRouter, Query, Path

from kme.database.db import generate
from kme.model import KeyContainer, Key, KeyRequest

router: Final[APIRouter] = APIRouter(tags=["enc_keys"])


@router.get(
    path="/{slave_SAE_ID}/enc_keys",
    summary="Get key",
    response_model=KeyContainer,
    response_model_exclude_none=True,
)
async def get_key(
    slave_SAE_ID: str,
    number: int = Query(default=1, description="Number of keys requested", ge=1),
    size: int = Query(default=64, description="Size of each key in bits", ge=1),
) -> KeyContainer:
    """
    Returns Key container data from the kme to the calling master SAE. The
    calling master SAE may supply Key request data to specify the
    requirement on Key container data. The slave SAE specified by the
    slave_SAE_ID parameter may subsequently request matching keys from a
    remote kme using key_ID identifiers from the returned Key container.
    """
    new_keys: Final[list[Key]] = []
    for _ in range(number):
        new_key: Key = await generate(size, frozenset([url_decode(slave_SAE_ID)]))
        new_keys.append(new_key)

    return KeyContainer(keys=tuple(new_keys))


@router.post(
    path="/{slave_SAE_ID}/enc_keys",
    summary="Post key",
    response_model=KeyContainer,
    response_model_exclude_none=True,
)
async def post_key(
    key_request: KeyRequest,
    slave_SAE_ID: str = Path(..., description="URL-encoded SAE ID of slave SAE"),
) -> KeyContainer:
    """
    Returns Key container data from the kme to the calling master SAE. Key
    container data contains one or more keys. The calling master SAE may
    supply Key request data to specify the requirement on Key container
    data. The slave SAE specified by the slave_SAE_ID parameter may
    subsequently request matching keys from a remote kme using key_ID
    identifiers from the returned Key container.
    """
    new_keys: Final[list[Key]] = []
    for _ in range(key_request.number):
        new_key: Key = await generate(
            key_request.size,
            frozenset(
                (url_decode(slave_SAE_ID), *key_request.additional_slave_SAE_IDs)
            ),
            *key_request.extension_mandatory,
            *key_request.extension_optional
        )

        new_keys.append(new_key)

    return KeyContainer(keys=tuple(new_keys))

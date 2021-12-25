from typing import Final, Any
from uuid import UUID

import pytest
from httpx import AsyncClient as Client, Response

from kme.configs import Config
from kme.errors import UnsupportedExtensionError, KeyNotFoundError, \
    SizeNotMultipleOfEightError
from kme.model import KeyContainer, KeyRequest, KeyIDs, KeyIDsKeyIDs
from kme.model.errors import Error

pytestmark = pytest.mark.asyncio


async def test_get_key(client: Client) -> None:
    """Test case for get_key"""
    slave_sae_id: Final[str] = 'slave_sae_id_example'

    response: Final[Response] = await client.get(
        url=f'{Config.BASE_URL}/{slave_sae_id}/enc_keys')

    key_container: Final[KeyContainer] = KeyContainer(**response.json())

    assert response.status_code == 200
    assert len(key_container.keys) == 1


async def test_get_key_with_invalid_number(client: Client) -> None:
    """get_key should return 400 if the given number is negative."""
    slave_sae_id: Final[str] = 'slave_sae_id_example'
    number: Final[int] = -1

    response: Final[Response] = await client.get(
        url=f'{Config.BASE_URL}/{slave_sae_id}/enc_keys',
        params={"number": number}
    )

    assert response.status_code == 400


async def test_get_key_with_key_i_ds(client: Client) -> None:
    """Test case for get_key_with_key_i_ds"""
    master_sae_id: Final[str] = "master_sae_id_example"
    key_id: Final[str] = "bc490419-7d60-487f-adc1-4ddcc177c139"

    response: Final[Response] = await client.get(
        url=f'{Config.BASE_URL}/{master_sae_id}/dec_keys',
        params={"key_ID": key_id}
    )

    key_container: Final[KeyContainer] = KeyContainer(**response.json())

    assert response.status_code == 200
    assert len(key_container.keys) == 1


async def test_get_key_with_key_i_ds_with_invalid_key_id(client: Client) \
        -> None:
    """
    get_key_with_key_id should return 400 if the given key id does not
    correspond to a key inside kme.
    """
    master_sae_id: Final[str] = "master_sae_id_example"
    invalid_key_id: Final[str] = "61536832-a1a7-4703-a85d-0de9bf909b29"

    response: Final[Response] = await client.get(
        url=f'{Config.BASE_URL}/{master_sae_id}/dec_keys',
        params={"key_ID": invalid_key_id}
    )

    error: Final[Error] = Error(**response.json())

    assert response.status_code == 400
    assert error.message == \
           KeyNotFoundError.detail


async def test_get_status(client: Client) -> None:
    """Test case for get_status"""
    slave_sae_id: Final[str] = 'slave_sae_id_example'

    response: Final[Response] = await client.get(
        url=f'{Config.BASE_URL}/{slave_sae_id}/status',
    )

    assert response.status_code == 200


async def test_post_key(client: Client) -> None:
    """Test case for post_key"""
    number: Final[int] = 5
    key_request: Final[KeyRequest] = KeyRequest(number=number)
    slave_sae_id: Final[str] = 'slave_sae_id_example'

    response: Final[Response] = await client.post(
        url=f'{Config.BASE_URL}/{slave_sae_id}/enc_keys',
        content=key_request.json(exclude_none=True),
    )

    key_container: Final[KeyContainer] = KeyContainer(**response.json())

    assert response.status_code == 200
    assert len(key_container.keys) == number


async def test_post_key_with_invalid_key_size(client: Client) -> None:
    """
    post_key should return 400 if the given key size is not a multiple of 8.
    """
    invalid_size: Final[int] = 10
    key_request: Final[KeyRequest] = KeyRequest(size=invalid_size)
    slave_sae_id: Final[str] = 'slave_sae_id_example'

    response: Final[Response] = await client.post(
        url=f'{Config.BASE_URL}/{slave_sae_id}/enc_keys',
        content=key_request.json(exclude_none=True),
    )

    error: Final[Error] = Error(**response.json())

    assert response.status_code == 400
    assert error.message == \
           SizeNotMultipleOfEightError.detail


async def test_post_key_with_key_i_ds(client: Client) -> None:
    """Test case for post_key_with_key_i_ds"""
    key_ids: Final[KeyIDs] = KeyIDs(
        key_IDs=tuple([KeyIDsKeyIDs(
            key_ID=UUID("bc490419-7d60-487f-adc1-4ddcc177c139"))]))
    master_sae_id: Final[str] = 'master_sae_id_example'

    response: Final[Response] = await client.post(
        url=f'{Config.BASE_URL}/{master_sae_id}/dec_keys',
        content=key_ids.json(),
    )

    key_container: Final[KeyContainer] = KeyContainer(**response.json())

    assert response.status_code == 200
    assert len(key_container.keys) == len(key_ids.key_IDs)


async def test_post_key_non_empty_extension_mandatory(client: Client) \
        -> None:
    """Test case for post_key with non-empty 'extension_mandatory'
    parameter. """
    extension_mandatory: Final[tuple[dict[str, Any], ...]] = \
        ({"ciao": "mamma"},)
    key_request: Final[KeyRequest] = KeyRequest(
        extension_mandatory=extension_mandatory
    )
    slave_sae_id: Final[str] = 'slave_sae_id_example'

    response: Final[Response] = await client.post(
        url=f'{Config.BASE_URL}/{slave_sae_id}/enc_keys',
        content=key_request.json(),
    )

    error: Final[Error] = Error(**response.json())

    assert response.status_code == 400
    assert error.message == \
           UnsupportedExtensionError.detail

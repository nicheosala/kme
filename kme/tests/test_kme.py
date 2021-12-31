from typing import Final

import pytest
from httpx import AsyncClient as Client, Response
from pydantic import ValidationError

from kme.configs import Config
from kme.encoder import dump
from kme.model import KeyContainer, KeyRequest, KeyIDs, KeyIDsKeyIDs
from kme.model.errors import Error, KeyNotFound
from kme.tests.examples import key_1, key_2

pytestmark = pytest.mark.asyncio


async def test_get_key(client: Client) -> None:
    """Test case for get_key"""
    slave_sae_id: Final[str] = "slave_sae_id_example"

    response: Final[Response] = await client.get(
        url=f"{Config.BASE_URL}/{slave_sae_id}/enc_keys"
    )

    key_container: Final[KeyContainer] = KeyContainer(**response.json())

    assert response.status_code == 200
    assert len(key_container.keys) == 1


async def test_get_key_with_invalid_number(client: Client) -> None:
    """get_key should return 400 if the given number is negative."""
    slave_sae_id: Final[str] = "slave_sae_id_example"
    number: Final[int] = -1

    response: Final[Response] = await client.get(
        url=f"{Config.BASE_URL}/{slave_sae_id}/enc_keys", params={"number": number}
    )

    assert response.status_code == 400


async def test_get_key_with_key_i_ds(client: Client, init_db: None) -> None:
    """Test case for get_key_with_key_i_ds"""
    master_sae_id: Final[str] = "master_sae_id_example"

    response: Final[Response] = await client.get(
        url=f"{Config.BASE_URL}/{master_sae_id}/dec_keys",
        params={"key_ID": str(key_1.key_id)},
    )

    key_container: Final[KeyContainer] = KeyContainer(**response.json())

    assert response.status_code == 200
    assert len(key_container.keys) == 1
    assert key_container.keys[0].key_ID == key_1.key_id


async def test_get_key_with_key_i_ds_with_invalid_key_id(client: Client) -> None:
    """
    get_key_with_key_id should return 400 if the given key id does not
    correspond to a key inside kme.
    """
    master_sae_id: Final[str] = "master_sae_id_example"
    invalid_key_id: Final[str] = "61536832-a1a7-4703-a85d-0de9bf909b29"

    response: Final[Response] = await client.get(
        url=f"{Config.BASE_URL}/{master_sae_id}/dec_keys",
        params={"key_ID": invalid_key_id},
    )

    error: Final[Error] = Error(**response.json())

    assert response.status_code == 400
    assert error.message == KeyNotFound.detail


async def test_get_status(client: Client) -> None:
    """Test case for get_status"""
    slave_sae_id: Final[str] = "slave_sae_id_example"

    response: Final[Response] = await client.get(
        url=f"{Config.BASE_URL}/{slave_sae_id}/status",
    )

    assert response.status_code == 200


async def test_post_key(client: Client) -> None:
    """Test case for post_key"""
    number: Final[int] = 5
    key_request: Final[KeyRequest] = KeyRequest(number=number)
    slave_sae_id: Final[str] = "slave_sae_id_example"

    response: Final[Response] = await client.post(
        url=f"{Config.BASE_URL}/{slave_sae_id}/enc_keys",
        json=dump(key_request),
    )

    key_container: Final[KeyContainer] = KeyContainer(**response.json())

    assert response.status_code == 200
    assert len(key_container.keys) == number


async def test_post_key_with_invalid_key_size(client: Client) -> None:
    """
    post_key should return 400 if the given key size is not a multiple of 8.
    """
    with pytest.raises(ValidationError):
        KeyRequest(size=10)


async def test_post_key_with_key_i_ds(client: Client, init_db: None) -> None:
    """Test case for post_key_with_key_i_ds"""
    key_ids: Final[KeyIDs] = KeyIDs(
        key_IDs=(KeyIDsKeyIDs(key_ID=key_1.key_id), KeyIDsKeyIDs(key_ID=key_2.key_id))
    )
    master_sae_id: Final[str] = "master_sae_id_example"

    response: Final[Response] = await client.post(
        url=f"{Config.BASE_URL}/{master_sae_id}/dec_keys",
        json=dump(key_ids),
    )

    key_container: Final[KeyContainer] = KeyContainer(**response.json())

    assert response.status_code == 200
    assert len(key_container.keys) == len(key_ids.key_IDs)
    assert key_1.key_id in (k.key_ID for k in key_container.keys)
    assert key_2.key_id in (k.key_ID for k in key_container.keys)


async def test_post_key_non_empty_extension_mandatory(client: Client) -> None:
    """Test case for post_key with non-empty 'extension_mandatory'
    parameter."""
    with pytest.raises(ValidationError):
        KeyRequest(extension_mandatory=({"ciao": "mamma"},))

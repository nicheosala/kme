import uuid
from asyncio import gather
from itertools import combinations
from typing import Final

import pytest
from httpx import AsyncClient, Response
from pydantic import ValidationError

from kme.configs import Config
from kme.database import orm
from kme.database.dbms import retrieve_key_material, Instruction
from kme.encoder import dump, load
from kme.model import KeyContainer, KeyRequest, KeyIDs, KeyIDsKeyIDs, OpenSessionResponse
from kme.model.errors import Error, KeyNotFound
from kme.model.open_session_request import OpenSessionRequest
from kme.tests.examples import key_1, key_2, qos
from kme.utils import bit_length_b64

pytestmark = pytest.mark.asyncio


async def test_get_key(client: AsyncClient, init_blocks: None) -> None:
    """Test case for get_key"""
    slave_sae_id: Final[str] = "slave_sae_id_example"

    response: Final[Response] = await client.get(
        url=f"{Config.BASE_URL}/{slave_sae_id}/enc_keys"
    )

    key_container: Final[KeyContainer] = KeyContainer(**response.json())

    assert response.status_code == 200
    assert len(key_container.keys) == 1


async def test_get_key_with_fixed_size(client: AsyncClient, init_blocks: None) -> None:
    """Test case for get_key fixing key size."""
    slave_sae_id: Final[str] = "slave_sae_id_example"
    size: Final[int] = 256

    response: Final[Response] = await client.get(
        url=f"{Config.BASE_URL}/{slave_sae_id}/enc_keys", params={"size": size}
    )

    key_container: Final[KeyContainer] = KeyContainer(**response.json())

    assert response.status_code == 200
    assert len(key_container.keys) == 1
    assert all(bit_length_b64(k.key) == size for k in key_container.keys)


async def test_get_key_with_invalid_number(client: AsyncClient) -> None:
    """get_key should return 400 if the given number is negative."""
    slave_sae_id: Final[str] = "slave_sae_id_example"
    number: Final[int] = -1

    response: Final[Response] = await client.get(
        url=f"{Config.BASE_URL}/{slave_sae_id}/enc_keys", params={"number": number}
    )

    assert response.status_code == 400


async def test_get_key_with_key_i_ds(
    client: AsyncClient, init_keys: None, init_blocks: None
) -> None:
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


async def test_get_key_with_key_i_ds_with_invalid_key_id(client: AsyncClient) -> None:
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


async def test_get_status(client: AsyncClient) -> None:
    """Test case for get_status"""
    slave_sae_id: Final[str] = "slave_sae_id_example"

    response: Final[Response] = await client.get(
        url=f"{Config.BASE_URL}/{slave_sae_id}/status",
    )

    assert response.status_code == 200


async def test_post_key(client: AsyncClient, init_blocks: None) -> None:
    """Test case for post_key"""
    number: Final[int] = 2
    size: Final[int] = 64
    key_request: Final[KeyRequest] = KeyRequest(number, size)
    slave_sae_id: Final[str] = "slave_sae_id_example"

    response: Final[Response] = await client.post(
        url=f"{Config.BASE_URL}/{slave_sae_id}/enc_keys",
        json=dump(key_request),
    )

    key_container: Final[KeyContainer] = KeyContainer(**response.json())

    assert response.status_code == 200
    assert len(key_container.keys) == number
    assert all(bit_length_b64(k.key) == size for k in key_container.keys)


async def test_post_key_with_invalid_key_size(client: AsyncClient) -> None:
    """
    post_key should return 400 if the given key size is not a multiple of 8.
    """
    with pytest.raises(ValidationError):
        KeyRequest(size=10)


async def test_post_key_with_key_i_ds(
    client: AsyncClient, init_blocks: None, init_keys: None
) -> None:
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


async def test_post_key_non_empty_extension_mandatory(client: AsyncClient) -> None:
    """Test case for post_key with non-empty 'extension_mandatory'
    parameter."""
    with pytest.raises(ValidationError):
        KeyRequest(extension_mandatory=({"ciao": "mamma"},))


async def test_response_and_database_coherency(
    client: AsyncClient, init_blocks: None
) -> None:
    response = await client.get(
        url=f"{Config.BASE_URL}/example_sae_id/enc_keys", params={"size": 40}
    )

    key_container: Final[KeyContainer] = KeyContainer(**response.json())
    response_key = key_container.keys[0]

    db_key: orm.Key = await orm.Key.objects.get(key_id=response_key.key_ID)
    db_key_material = await retrieve_key_material(db_key.instructions)

    assert db_key_material == response_key.key


async def test_non_overlapping_instructions(
    client: AsyncClient, init_blocks: None
) -> None:
    """Check that the instructions inside the database are not overlapping."""
    url = f"{Config.BASE_URL}/example_sae_id/enc_keys"
    requests = (client.get(url, params={"size": 64}) for _ in range(5))
    responses = await gather(*requests)

    orm_keys: list[orm.Key] = await orm.Key.objects.all()
    instructions: list[Instruction] = []
    for k in orm_keys:
        instructions.extend(load(k.instructions, tuple[Instruction, ...]))

    assert all(r.status_code == 200 for r in responses)
    assert all(disjoint(a, b) for a, b in combinations(instructions, 2))


def disjoint(a: Instruction, b: Instruction) -> bool:
    """Check if two instructions are disjointed."""
    return a.block_id != b.block_id or not (
        set(range(a.start, a.end)) & set(range(b.start, b.end))
    )


async def test_open_key_session(client: AsyncClient) -> None:
    """Tests an app requesting a connection to another app."""
    app_registration: Final[OpenSessionRequest] = OpenSessionRequest(src=uuid.uuid4(), dst=uuid.uuid4(), qos=qos)

    response: Final[Response] = await client.post(
        url=f"/open_key_session",
        json=dump(app_registration)
    )

    waiting_response: Final[OpenSessionResponse] = OpenSessionResponse(**response.json())

    assert response.status_code == 200
    assert isinstance(waiting_response.key_stream_id, type(uuid.uuid4()))

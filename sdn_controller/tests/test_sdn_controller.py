import uuid
from typing import Final

import pytest

from httpx import AsyncClient, Response

from sd_qkd_node.model.new_kme import NewKmeRequest, NewKmeResponse
from sdn_controller.encoder import dump
from sdn_controller.model.new_app import NewAppRequest, WaitingForApp
from sdn_controller.tests.examples import qos

pytestmark = pytest.mark.asyncio


async def test_new_app(client: AsyncClient) -> None:
    """Tests SDN Agent's request to the Controller to connect two apps."""
    kme_registration: Final[NewKmeRequest] = NewKmeRequest(
        ip="localhost", port=5000
    )
    response1: Final[Response] = await client.post(
        url=f"/new_kme",
        json=dump(kme_registration)
    )

    kme: Final[NewKmeResponse] = NewKmeResponse(**response1.json())

    app_registration: Final[NewAppRequest] = NewAppRequest(
        src_flag=True,
        src=uuid.uuid4(),
        dst=uuid.uuid4(),
        kme=kme.kme_id,
        qos=qos
    )

    response2: Final[Response] = await client.post(
        url=f"/new_app",
        json=dump(app_registration)
    )

    new_app_response: Final[WaitingForApp] = WaitingForApp()

    assert response2.status_code == 200
    assert new_app_response.wait is True


async def test_new_kme(client: AsyncClient) -> None:
    """Tests SDN Agent's request to the Controller to connect two apps."""
    kme_registration: Final[NewKmeRequest] = NewKmeRequest(
        ip="localhost",
        port=5000
    )

    response: Final[Response] = await client.post(
        url=f"/new_kme",
        json=dump(kme_registration)
    )

    new_kme_response: Final[NewKmeResponse] = NewKmeResponse(**response.json())

    assert response.status_code == 200
    assert isinstance(new_kme_response.kme_id, type(uuid.uuid4()))

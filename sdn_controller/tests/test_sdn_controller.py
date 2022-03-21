import uuid
from typing import Final

import pytest

from httpx import AsyncClient, Response

from sdn_controller.encoder import dump
from sdn_controller.model.new_app_request import NewAppRequest
from sdn_controller.model.new_app_response import NewAppResponse
from sdn_controller.tests.examples import qos

pytestmark = pytest.mark.asyncio


async def test_new_app(client: AsyncClient) -> None:
    """Tests SDN Agent's request to the Controller to connect two apps."""
    app_registration: Final[NewAppRequest] = NewAppRequest(
        src=uuid.uuid4(),
        dst=uuid.uuid4(),
        kme="Alice",
        qos=qos
    )

    response: Final[Response] = await client.post(
        url=f"/new_app",
        json=dump(app_registration)
    )

    new_app_response: Final[NewAppResponse] = NewAppResponse(**response.json())

    assert response.status_code == 200
    assert isinstance(new_app_response.key_stream_id, type(uuid.uuid4()))

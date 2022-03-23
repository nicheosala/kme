import asyncio
import logging
from typing import Final

from httpx import AsyncClient, Response
from uvicorn import run

from kme import kme_app
from sdn_controller import sdn_app
from kme.encoder import dump
from kme.model.new_kme import NewKmeRequest, NewKmeResponse
from kme.channel.qc_server import QCServer
from kme.configs import Config


def set_logging() -> None:
    """Initialize logging."""
    logger = logging.getLogger("kme")
    logger.setLevel(logging.DEBUG if Config.DEBUG else logging.INFO)
    logger.addHandler(logging.StreamHandler())


async def connect_to_controller():
    async with AsyncClient(app=sdn_app.app, base_url=Config.SDN_CONTROLLER_ADDRESS) as client:
        response: Final[Response] = await client.post(
            url=f"{Config.SDN_CONTROLLER_ADDRESS}/new_kme",
            json=dump(NewKmeRequest(ip=Config.KME_IP, port=Config.SAE_TO_KME_PORT))
        )
        kme: Final[NewKmeResponse] = NewKmeResponse(**response.json())
        Config.KME_ID = kme.kme_id
        logging.getLogger("kme").info(msg=f"Kme added to SDN Controller, with id: {kme.kme_id}")


if __name__ == "__main__":
    set_logging()
    with QCServer():
        asyncio.run(connect_to_controller())
        # noinspection PyTypeChecker
        run(app=kme_app.app, host=Config.KME_IP, port=Config.SAE_TO_KME_PORT)

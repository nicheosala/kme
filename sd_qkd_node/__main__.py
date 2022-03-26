import asyncio
import logging
from typing import Final

from httpx import AsyncClient, Response
from uvicorn import run

from sd_qkd_node import kme_app
from sd_qkd_node.utils import Bcolors
from sd_qkd_node.encoder import dump
from sd_qkd_node.model.new_kme import NewKmeRequest, NewKmeResponse
from sd_qkd_node.channel.qc_server import QCServer
from sd_qkd_node.configs import Config


def set_logging() -> None:
    """Initialize logging."""
    logger = logging.getLogger("sd_qkd_node")
    logger.setLevel(logging.DEBUG if Config.DEBUG else logging.INFO)
    logger.addHandler(logging.StreamHandler())


async def connect_to_controller() -> None:
    async with AsyncClient() as client:
        response: Final[Response] = await client.post(
            url=f"{Config.SDN_CONTROLLER_ADDRESS}/new_kme",
            json=dump(NewKmeRequest(ip=Config.KME_IP, port=Config.SAE_TO_KME_PORT))
        )
        kme: Final[NewKmeResponse] = NewKmeResponse(**response.json())
        Config.KME_ID = kme.kme_id
        logging.getLogger("sd_qkd_node").info(
            f"\n{Bcolors.OKGREEN}Kme id:{Bcolors.ENDC} {Bcolors.BOLD}{kme.kme_id}{Bcolors.ENDC}\n"
        )


if __name__ == "__main__":
    set_logging()
    with QCServer():
        asyncio.run(connect_to_controller())
        # noinspection PyTypeChecker
        run(app=kme_app.app, host=Config.KME_IP, port=Config.SAE_TO_KME_PORT)

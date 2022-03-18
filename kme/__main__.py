import logging
from argparse import ArgumentParser, Namespace

from uvicorn import run

from kme import app
from kme.channel.qc_server import QCServer
from kme.configs import Config


def set_logging() -> None:
    """Initialize logging."""
    logger = logging.getLogger("kme")
    logger.setLevel(logging.DEBUG if Config.DEBUG else logging.INFO)
    logger.addHandler(logging.StreamHandler())


if __name__ == "__main__":
    set_logging()
    with QCServer():
        # noinspection PyTypeChecker
        run(app=app, host=Config.KME_IP, port=Config.SAE_TO_KME_PORT)

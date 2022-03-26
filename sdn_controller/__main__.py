import logging

from uvicorn import run

from sdn_controller import sdn_app
from sdn_controller.configs import Config


def set_logging() -> None:
    """Initialize logging."""
    logger = logging.getLogger("sdn_controller")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())


if __name__ == "__main__":
    set_logging()
    # noinspection PyTypeChecker
    run(app=sdn_app.app, host=Config.IP, port=Config.PORT)

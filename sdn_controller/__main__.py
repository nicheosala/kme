import logging

from uvicorn import run

from sdn_controller import app
from sdn_controller.configs import Config


def set_logging() -> None:
    """Initialize logging."""
    logger = logging.getLogger("ctrl")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())


if __name__ == "__main__":
    set_logging()
    # with Controller():
        # pass
        # noinspection PyTypeChecker
    run(app=app, host=Config.IP, port=Config.PORT)

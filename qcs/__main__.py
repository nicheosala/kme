"""Start a quantum channel simulator."""
import logging
from threading import Event

from qcs import Simulator
from qcs.configs import Config


def set_logging() -> None:
    """Initialize logging."""
    logger = logging.getLogger("qcs")
    logger.setLevel(logging.DEBUG if Config.DEBUG else logging.INFO)
    logger.addHandler(logging.StreamHandler())


if __name__ == "__main__":
    set_logging()
    with Simulator():
        try:
            Event().wait()
        except KeyboardInterrupt:
            exit()

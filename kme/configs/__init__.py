"""Configuration parameters for KME."""
import logging
from os import environ
from typing import Final

from kme.configs.configs import Base, Dev, Test, Prod


def __set_config() -> Base:
    """Initialize the configurtation."""
    env: str | None = environ.get('env')
    if env == 'prod':
        return Prod()
    elif env == 'test':
        return Test()
    else:
        return Dev()


Config: Final[Base] = __set_config()


def __set_logging() -> None:
    """Initialize logging."""
    env: str | None = environ.get('env')
    if env == 'dev':
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)


__set_logging()

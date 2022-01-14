import logging
from os import environ
from typing import Final

from qcs.configs.configs import Base, Dev, Test, Prod


def __set_config() -> Base:
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
    env: str | None = environ.get("env")
    if env == "dev":
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)


__set_logging()

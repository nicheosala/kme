import logging
from os import environ
from typing import Final

from kme.configs.configs import Base, Dev, Test, Prod


def __set_config() -> Base:
    env: str | None = environ.get('env')
    if env == 'prod':
        return Prod()
    elif env == 'test':
        logging.basicConfig(level=logging.DEBUG)
        return Test()
    else:
        logging.basicConfig(level=logging.DEBUG)
        return Dev()


Config: Final[Base] = __set_config()


def __set_logging() -> None:
    env: str | None = environ.get('env')
    if env in ('test', 'dev'):
        logging.basicConfig(level=logging.DEBUG)


__set_logging()

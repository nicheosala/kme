from os import environ
from typing import Final

from kme.configs.configs import Base, Dev, Test, Prod


def __set_config() -> Base:
    env: str | None = environ.get('env')
    if env == 'prod':
        return Prod()
    elif env == 'test':
        return Test()
    else:
        return Dev()


Config: Final[Base] = __set_config()

from argparse import ArgumentParser
from dataclasses import dataclass
from typing import Final


@dataclass(slots=True, init=False)
class BaseConfig:
    ENV = 'development'
    API_PATH = 'api/openapi.yaml'
    BASE_URL = '/api/v1/keys'
    HOST = 'localhost'
    DEBUG = False
    TESTING = False
    APP_PORT = 5000
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_WARN_20 = True
    PROPAGATE_EXCEPTIONS = False


@dataclass(slots=True, init=False)
class Production(BaseConfig):
    ENV = 'production'
    DEBUG = False
    TESTING = False


@dataclass(slots=True, init=False)
class Development(BaseConfig):
    ENV = 'development'
    DEBUG = True
    TESTING = False


@dataclass(slots=True, init=False)
class Test(BaseConfig):
    ENV = 'test'
    DEBUG = True
    TESTING = True


def __set_config() -> BaseConfig:
    parser: Final[ArgumentParser] = ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-dev', action='store_true',
                       help='Start kme in development mode.')
    group.add_argument('-prod', action='store_true',
                       help='Start kme in production mode.')
    group.add_argument('-test', action='store_true',
                       help='Start kme in test mode.')
    args = parser.parse_args()
    if args.prod:
        return Production()
    elif args.test:
        return Test()
    else:
        return Development()


Config: BaseConfig = __set_config()

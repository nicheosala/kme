from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Final


class BaseConfig(ABC):
    API_PATH = 'api/openapi.yaml'
    BASE_URL = '/api/v1/keys'
    HOST = 'localhost'
    APP_PORT = 5000
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_WARN_20 = True
    PROPAGATE_EXCEPTIONS = False

    @property
    @abstractmethod
    def ENV(self) -> str:
        pass

    @property
    @abstractmethod
    def DEBUG(self) -> bool:
        pass

    @property
    @abstractmethod
    def TESTING(self) -> bool:
        pass

    @property
    @abstractmethod
    def DATABASE_URL(self) -> str:
        pass


@dataclass(frozen=True, slots=True, init=False)
class ProductionConfig(BaseConfig):
    ENV = 'production'
    DEBUG = False
    TESTING = False
    DATABASE_URL = 'sqlite:///db'


@dataclass(frozen=True, slots=True, init=False)
class DevelopmentConfig(BaseConfig):
    ENV = 'development'
    DEBUG = True
    TESTING = False
    DATABASE_URL = 'sqlite:///devdb'


@dataclass(frozen=True, slots=True, init=False)
class TestConfig(BaseConfig):
    ENV = 'test'
    DEBUG = True
    TESTING = True
    DATABASE_URL = 'sqlite:///testdb'


Config: Final[BaseConfig] = DevelopmentConfig()

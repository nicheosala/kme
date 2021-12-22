from abc import ABC, abstractmethod
from dataclasses import dataclass


class Base(ABC):
    BASE_URL = '/api/v1/keys'
    HOST = 'localhost'
    PORT = 5000

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
class Prod(Base):
    DEBUG = False
    TESTING = False
    DATABASE_URL = 'sqlite:///db'


@dataclass(frozen=True, slots=True, init=False)
class Dev(Base):
    DEBUG = True
    TESTING = False
    DATABASE_URL = 'sqlite:///devdb'


@dataclass(frozen=True, slots=True, init=False)
class Test(Base):
    DEBUG = False
    TESTING = True
    DATABASE_URL = 'sqlite:///testdb'

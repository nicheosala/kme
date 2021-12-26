from abc import ABC, abstractmethod
from dataclasses import dataclass


class Base(ABC):
    HOST = 'localhost'
    PORT = 9998
    COMPATIBILITY_MODE = True

    @property
    @abstractmethod
    def DEBUG(self) -> bool:
        pass

    @property
    @abstractmethod
    def TESTING(self) -> bool:
        pass


@dataclass(frozen=True, slots=True, init=False)
class Prod(Base):
    DEBUG = False
    TESTING = False


@dataclass(frozen=True, slots=True, init=False)
class Dev(Base):
    DEBUG = True
    TESTING = False


@dataclass(frozen=True, slots=True, init=False)
class Test(Base):
    DEBUG = True
    TESTING = True

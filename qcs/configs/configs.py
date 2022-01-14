from abc import ABC, abstractmethod
from dataclasses import dataclass
from os import environ


class Base(ABC):
    PORT = 9998
    COMPATIBILITY_MODE = True

    @property
    def HOST(self) -> str:
        """The host where kme will run."""
        return "0.0.0.0" if environ.get("DOCKER_RUNNING") == "true" else "localhost"

    @property
    @abstractmethod
    def POLL_INTERVAL(self) -> float:
        """The simulator polls for shutdown every POLL_INTERVAL seconds."""

    @property
    @abstractmethod
    def DEBUG(self) -> bool:
        """Tell if debug mode is active or not."""

    @property
    @abstractmethod
    def TESTING(self) -> bool:
        """Tell if testing mode is active or not."""


@dataclass(frozen=True, slots=True, init=False)
class Prod(Base):
    DEBUG = False
    TESTING = False
    POLL_INTERVAL = 0.5


@dataclass(frozen=True, slots=True, init=False)
class Dev(Base):
    DEBUG = True
    TESTING = False
    POLL_INTERVAL = 0.001


@dataclass(frozen=True, slots=True, init=False)
class Test(Base):
    DEBUG = True
    TESTING = True
    POLL_INTERVAL = 0.001

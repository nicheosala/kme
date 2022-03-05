"""Configurations for KME."""
from abc import ABC, abstractmethod
from dataclasses import dataclass

from pydantic import PostgresDsn


class Base(ABC):
    """Base Config class."""

    KME_ID = "Alice"

    HOST = "localhost"
    PORT = 5000

    QC_HOST = "localhost"
    QC_PORT = 9998

    COMPANION_URL = "http://localhost:3000"

    BASE_URL = "/api/v1/keys"

    """
    A block inside the local database cannot be exploited to generate new keys
    if the difference between "now" and its timestamp is greater than TTL.
    """
    TTL = 120

    # Status
    MIN_KEY_SIZE = 8
    MAX_KEY_SIZE = 8192
    DEFAULT_KEY_SIZE = 256
    MAX_KEY_PER_REQUEST = 10
    STORED_KEY_COUNT = 10
    MAX_KEY_COUNT = 10
    MAX_SAE_ID_COUNT = 10

    # Key request
    SUPPORTED_EXTENSION_PARAMS: frozenset[str] = frozenset()

    @property
    @abstractmethod
    def DEBUG(self) -> bool:
        """Debug flag."""

    @property
    @abstractmethod
    def TESTING(self) -> bool:
        """Test flag."""

    LOCAL_DB_URL = "sqlite:///local_db"

    @property
    @abstractmethod
    def SHARED_DB_URL(self) -> str:
        """URL for shared database connection."""

    @property
    @abstractmethod
    def POLL_INTERVAL(self) -> float:
        """The qcserver polls for shutdown every POLL_INTERVAL seconds."""


@dataclass(frozen=True, slots=True, init=False)
class Prod(Base):
    """Configuration for production environment."""

    DEBUG = False
    TESTING = False
    POLL_INTERVAL = 0.5

    @property
    def SHARED_DB_URL(self) -> str:
        """URL for database connection.

        1. Install PostgreSQL
        2. `sudo -i -u postgres psql`
        3. `ALTER ROLE postgres WITH PASSWORD 'very_strong_password';`
        4. `CREATE DATABASE prod_db;`
        """
        url: str = PostgresDsn.build(
            scheme="postgresql",
            user="postgres",
            password="secret",
            host="localhost",
            port="5432",
            path="/prod_db",
        )
        return url


@dataclass(frozen=True, slots=True, init=False)
class Dev(Base):
    """Configuration for development environment."""

    DEBUG = True
    TESTING = False
    SHARED_DB_URL = "sqlite:///devdb"
    POLL_INTERVAL = 0.001


@dataclass(frozen=True, slots=True, init=False)
class Test(Base):
    """Configuration for testing environment."""

    DEBUG = False
    TESTING = True
    SHARED_DB_URL = "sqlite:///testdb"
    POLL_INTERVAL = 0.001

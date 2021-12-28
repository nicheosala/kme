"""Configurations for KME."""
from abc import ABC, abstractmethod
from dataclasses import dataclass

from pydantic import PostgresDsn


class Base(ABC):
    """Base Config class."""

    BASE_URL = '/api/v1/keys'
    HOST = 'localhost'
    PORT = 5000
    MIN_KEY_SIZE = 8
    MAX_KEY_SIZE = 8192
    DEFAULT_KEY_SIZE = 256
    MAX_KEY_PER_REQUEST = 10

    @property
    @abstractmethod
    def DEBUG(self) -> bool:
        """Debug flag."""
        pass

    @property
    @abstractmethod
    def TESTING(self) -> bool:
        """Test flag."""
        pass

    @property
    @abstractmethod
    def DATABASE_URL(self) -> str:
        """URL for database connection."""
        pass


@dataclass(frozen=True, slots=True, init=False)
class Prod(Base):
    """Configuration for production environment."""

    DEBUG = False
    TESTING = False

    @property
    def DATABASE_URL(self) -> str:
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
            path="/prod_db"
        )
        return url


@dataclass(frozen=True, slots=True, init=False)
class Dev(Base):
    """Configuration for development environment."""

    DEBUG = True
    TESTING = False
    DATABASE_URL = 'sqlite:///devdb'


@dataclass(frozen=True, slots=True, init=False)
class Test(Base):
    """Configuration for testing environment."""

    DEBUG = False
    TESTING = True
    DATABASE_URL = 'sqlite:///testdb'

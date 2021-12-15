from dataclasses import dataclass


@dataclass(frozen=True, slots=True, init=False)
class Config:
    API_PATH = 'api/openapi.yaml'
    BASE_URL = '/api/v1/keys'
    HOST = 'localhost'
    DEBUG = False
    TESTING = False
    APP_PORT = 5000
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = False


@dataclass(frozen=True, slots=True, init=False)
class Production(Config):
    ENV = 'production'
    DEBUG = False
    TESTING = False


@dataclass(frozen=True, slots=True, init=False)
class Development(Config):
    ENV = 'development'
    DEBUG = True
    TESTING = False


@dataclass(frozen=True, slots=True, init=False)
class Test(Config):
    ENV = 'test'
    DEBUG = True
    TESTING = True

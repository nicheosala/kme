from dataclasses import dataclass


@dataclass(frozen=True, slots=True, init=False)
class Config:
    DEBUG = False
    TESTING = False
    APP_PORT = 5000


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

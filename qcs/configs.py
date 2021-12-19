from dataclasses import dataclass


@dataclass(frozen=True, slots=True, init=False)
class Config:
    SERVER_HOST = 'localhost'
    SERVER_PORT = 9998
    DEBUG = False
    TESTING = False
    COMPATIBILITY_MODE = False


@dataclass(frozen=True, slots=True, init=False)
class Production(Config):
    DEBUG = False
    TESTING = False


@dataclass(frozen=True, slots=True, init=False)
class Development(Config):
    DEBUG = True
    TESTING = False


@dataclass(frozen=True, slots=True, init=False)
class Test(Config):
    DEBUG = True
    TESTING = True

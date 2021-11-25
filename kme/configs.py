import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True, init=False)
class Config:
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
    DEBUG = False
    TESTING = False
    APP_PORT = 5000


@dataclass(frozen=True, slots=True, init=False)
class Production(Config):
    ENV = 'production'
    DEBUG = False
    DB_NAME = 'production.db'
    DB_PATH = os.path.join(Config.DATA_DIR, DB_NAME)


@dataclass(frozen=True, slots=True, init=False)
class Development(Config):
    ENV = 'development'
    DEBUG = True
    DB_NAME = 'development.db'
    DB_PATH = os.path.join(Config.DATA_DIR, DB_NAME)


@dataclass(frozen=True, slots=True, init=False)
class Test(Config):
    ENV = 'test'
    DEBUG = True
    TESTING = True

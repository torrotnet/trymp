# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import logging
import os
from service_api.constants import DEFAULT_SERVICE_NAME


class Config:
    DB_SERVICE_NAME = os.environ.get("DB_SERVICE_NAME", "/msp/database/mongodb")
    DB_PORT = os.environ.get("DB_PORT", 27017)
    DEFAULT_DB = os.environ.get("DEFAULT_DB", "default")
    DB_URI_FORMAT = "mongodb://{user}:{password}@{host}:{port}/{db}"
    SERVICE_NAME = DEFAULT_SERVICE_NAME
    DEBUG = False
    LOG_FORMAT = "%(asctime)s %(levelname)8s %(message)s "
    LOG_DATEFMT = "%Y-%m-%dT%H:%M:%S"
    LOG_LEVEL = logging.DEBUG

    START_EXECUTE_LOG_MESSAGE = '{} start execution'
    COMPLETE_EXECUTE_LOG_MESSAGE = '{} complete execution at {:f} ms'


class ProdConfig(Config):
    """Production configuration."""

    LOG_FORMAT = (
        "%(asctime)s %(levelname)8s %(funcName)20s %(message)s %(type)s %(client)s %(user)s %(crud)s %(version)s"
    )
    LOG_LEVEL = logging.INFO


class DevConfig(Config):
    """Development configuration."""

    DEBUG = True


class QCConfig(Config):
    DEBUG = True


ENV_2_CONFIG = {"dev": DevConfig, "qc": QCConfig, "prod": ProdConfig}


def runtime_config(config=None):
    if config is None:
        env = os.environ.get("APP_ENV", "dev")
        assert env in ENV_2_CONFIG, "Unknown APP_ENV value: " + env
        config = ENV_2_CONFIG[env]

    return config

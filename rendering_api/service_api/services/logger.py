# -*- coding: utf-8 -*-
"""execution logger."""
import sys
from functools import wraps

from sanic.app import Sanic
from time import time

__server_instance = None


def register_server(app: Sanic):
    global __server_instance
    __server_instance = app


def get_logger(name):
    """Configures logger to match standard logging format Requires python-json-logger >= 0.1.5"""

    import logging
    from pythonjsonlogger import jsonlogger

    log = logging.getLogger(name)
    if not log.handlers:
        handler = logging.StreamHandler(sys.stdout)
        log_level = __server_instance.config.get("LOG_LEVEL")
        log_format = __server_instance.config.get("LOG_FORMAT")
        handler.setFormatter(jsonlogger.JsonFormatter(log_format))
        handler.setLevel(logging.DEBUG)
        log.addHandler(handler)
        log.setLevel(log_level)

    # Note: Gunicorn expects your logger to have a close_on_exec() method
    def just_pass():
        pass

    log.close_on_exec = just_pass

    return log


class LoggerWrapper:

    def __getattr__(self, item):
        log = get_logger(__name__)
        if hasattr(log, item):
            return getattr(log, item)
        else:
            raise AttributeError("Logger doesn't have attribute {}".format(item))


def log_execution(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_msg = __server_instance.config.get('START_EXECUTE_LOG_MESSAGE', "{}")
        complete_msg = __server_instance.config.get('COMPLETE_EXECUTE_LOG_MESSAGE', "{}, {}")

        logger.debug(start_msg.format(func.__qualname__))
        time_start = time()

        result = func(*args, **kwargs)

        time_complete = time()
        logger.debug(complete_msg.format(func.__qualname__, (time_complete - time_start) * 1000))

        return result
    return wrapper


logger = LoggerWrapper()

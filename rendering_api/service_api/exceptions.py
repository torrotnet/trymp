from traceback import format_exc

from sanic.app import Sanic
from sanic.exceptions import SanicException
from sanic.response import json

from service_api.services.logger import logger


def setup_exception_handler(app: Sanic):
    app.exception(Exception)(default_exception_handler)


def default_exception_handler(request, exception):
    logger.error(format_exc())
    if issubclass(type(exception), ApplicationError):
        message = str(exception)
    else:
        message = repr(exception)
    return json(
        {"error_message": message},
        status=getattr(exception, "status_code", 500),
        headers=getattr(exception, "headers", {"Content-type": "application/json"}),
    )


class ApplicationError(SanicException):
    pass


class AuthorizationError(ApplicationError):
    status_code = 401


class BadRequest(ApplicationError):
    status_code = 400


class UnprocessableEntity(ApplicationError):
    status_code = 422


class NotFoundException(ApplicationError):
    status_code = 404


class LockedException(ApplicationError):
    status_code = 423

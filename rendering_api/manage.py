#! /usr/bin/env python
import argparse
import asyncio
import os
import sys

from sanic.server import HttpProtocol

from service_api.app import app
from service_api.constants import COMMON_DB
from service_api.migrations.utils import (
    migrate_all,
    migrate,
    get_all_migrations,
)
from service_api.services.logger import logger

SANIC_PREFIX = "SANIC_"


def get_common_db_name():
    logger.info(COMMON_DB)


def migrate_wrapper():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(migrate_all())
    loop.close()


def runserver(host, port):
    for k, v in os.environ.items():
        if k.startswith(SANIC_PREFIX):
            _, config_key = k.split(SANIC_PREFIX, 1)
            app.config[config_key] = v

    migrate_wrapper()

    class CGDPHttpProtocol(HttpProtocol):

        def __init__(self, *args, **kwargs):
            if "request_timeout" in kwargs:
                kwargs.pop("request_timeout")
            super().__init__(*args, request_timeout=300, **kwargs)

    app.run(host=host, port=port, protocol=CGDPHttpProtocol, debug=True)


def parse_args(args):
    parser = argparse.ArgumentParser(description="Sanic rest api skeleton", add_help=False)
    parser.add_argument("--help", action="help", help="show this help message and exit")

    subparsers = parser.add_subparsers(dest="command")

    sparser = subparsers.add_parser(runserver.__name__, add_help=False, help="Run server")
    sparser.add_argument("-h", "--host", dest="host", default="0.0.0.0", type=str, help="Host address")
    sparser.add_argument("-p", "--port", dest="port", default=8000, type=int, help="Host post")

    sparser = subparsers.add_parser(migrate_all.__name__, add_help=False, help="Make all migrations")
    sparser = subparsers.add_parser(migrate.__name__, add_help=False, help="Make concrete migration",)
    sparser.add_argument("-m", dest="migration", type=str, help="Migration name", choices=get_all_migrations())

    return parser.parse_args(args=args)


def main(args=None):

    parsed_args = parse_args(args or sys.argv[1:])
    if parsed_args.command == migrate_all.__name__:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(migrate_all())
        loop.close()
    elif parsed_args.command == migrate.__name__:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(migrate(parsed_args.migration))
        loop.close()
    elif parsed_args.command == runserver.__name__:
        runserver(parsed_args.host, parsed_args.port)


app.static('/static', './static')  # while in docker files from static will be served by ngnix
if __name__ == "__main__":
    try:
        main()
        logger.info("Service started")
    except Exception as e:
        logger.critical(
            "Unexpected exception occurred. Service is going to shutdown. Error message: {}".format(e),
            extra={"error_message": e},
        )
        exit(1)
    finally:
        logger.info("Service stopped.")

from typing import Tuple, Optional

from sanic.app import Sanic


async def release_engines():
    pass


async def close_engine(client_name: str):
    pass


def register_server(app: Sanic):
    global __server_instance
    __server_instance = app


async def db_uri(client_name: Optional[str] = None, host: Optional[str] = None) -> str:
    pass


def _create_engine(connection_url: str):
    pass


async def get_engine(client: Optional[str] = None, host: Optional[str] = None):
    pass


async def create_db(client_name: Optional[str] = None, host: Optional[str] = None) -> Tuple[str, int]:
    pass


async def create_common_db(host: Optional[str] = None) -> Tuple[str, int]:
    pass


async def drop_all_service_keyspaces():
    pass


async def drop_db(db_name, db_ip):
    pass

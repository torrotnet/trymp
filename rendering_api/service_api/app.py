from motor.motor_asyncio import AsyncIOMotorClient
from sanic.app import Sanic
from sanic_cors import CORS
from service_api import api_v1
from service_api.config import runtime_config
from service_api.constants import DEFAULT_SERVICE_NAME
from service_api.controllers import setup_controllers
from service_api.exceptions import setup_exception_handler
from service_api.services import logger, database

ALL = 'all'

app = Sanic(DEFAULT_SERVICE_NAME)
db_client = AsyncIOMotorClient


app.config.from_object(runtime_config())

cors = CORS(
    app,
    # resources={r"*": {"origin": "*"}},
    # expose_headers=[
    #     "Link, X-Pagination-Current-Page",
    #     "X-Pagination-Per-Page",
    #     "X-Pagination-Total-Count",
    #     "X-Client",
    #     "Authorization",
    #     "Content-Type",
    #     "X-Filename",
    # ],
)
api_v1.load_api(app)
logger.register_server(app=app)
setup_exception_handler(app)
database.register_server(app=app)


@app.middleware('request')
async def print_on_request(request):
    pass
    # client = request.match_info.get('client')
    # collection = request.match_info.get('collection')
    # if client and collection and not client == ALL:
    #     request.app.connect = get_collection_connect(request, client, collection)


@app.listener("after_server_start")
async def init(app: Sanic, loop):
    mongo_ip, mongo_port = 'mongodb', '27017'
    app.mongo_client = db_client("mongodb://{ip}:{port}/".format(
        ip=mongo_ip, port=mongo_port), io_loop=app.loop)


@app.listener("after_server_stop")
async def after_server_stop(app, loop):
    pass
    # await database.release_engines()


@app.listener("before_server_start")
async def before_server_start(app, loop):
    setup_controllers(app)

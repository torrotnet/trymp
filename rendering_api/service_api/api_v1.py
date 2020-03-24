from sanic import Blueprint
from sanic.app import Sanic
from sanic_swagger import swagger_blueprint, openapi_blueprint


def load_api(app: Sanic):
    from service_api.resources import (
        SmokeResources,
        HelloWorldView,
        # AllDataResourceView,
    )

    api_prefix = "/{service_name}/v1".format(service_name=app.config.get("SERVICE_NAME"))
    api_v1 = Blueprint("v1", url_prefix=api_prefix)

    # get the endpoints here
    api_v1.add_route(SmokeResources.as_view(), "/smoke", strict_slashes=False)
    api_v1.add_route(HelloWorldView.as_view(), "/hello-world", strict_slashes=False)
    # api_v1.add_route(AllDataResourceView.as_view(), '/all/<collection>',
    #                  strict_slashes=False)
    app.blueprint(api_v1)
    app.blueprint(openapi_blueprint)
    app.blueprint(swagger_blueprint)

from sanic_swagger import doc
from sanic.response import json
from sanic.views import HTTPMethodView


class SmokeResources(HTTPMethodView):

    @doc.summary('Smoke test')
    async def get(self, *args, **kwargs):
        """HTTP GET method for smoke test.

                Args:
                    *args: Anything.
                    **kwargs: Anything.

                Returns:
                    JSON data:
                        {"hello": "world"}

                """
        return json({"hello": "world"})

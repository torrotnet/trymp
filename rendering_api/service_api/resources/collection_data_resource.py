from service_api.resources.base_view import BaseDataResource
from service_api.services.logger import log_execution
from sanic_swagger import doc
from service_api.swagger_models.quieries import Query, Bulk


class HelloWorldView(BaseDataResource):

    @doc.summary("Hello world")
    @doc.consumes(Query, location='query')
    @log_execution
    async def get(self, request):
        # """HTTP GET method for all data resources.
        #
        # Args:
        #     request (sanic.request.Request): Sanic request object.
        #     collection (str): Collection name.
        #
        # Returns:
        #     sanic.response.HTTPResponse object with data found:
        #         {
        #             "data": [
        #                 {"id": "5c4ee1aba7e63a047e289077", ...},
        #                 ...
        #                 {"id": "5c4ee1aba7e63a047e28907n", ...}
        #             ],
        #             "response_datetime": "2019-01-28T11:43:10.436648",
        #             "status": "success"
        #         }
        #
        # """
        # params = self._validate_query(request.args).get('query')
        collection = 'Metadata'
        params = {}
        controller = request.app.controllers.CollectionDataController
        data = await controller.get_all(params, collection)

        return self.get_response(data)

from abc import abstractmethod
import datetime
from http import HTTPStatus

import sanic.request
from sanic import response
from sanic.constants import HTTP_METHODS
from sanic.views import HTTPMethodView
import simplejson
import ujson

from ..services.forms import query_parser
from ..services.json_encoder import CustomJSONEncoder
from ..services.utils import MongoIdConverter


class BaseView(HTTPMethodView):
    @staticmethod
    def _string_to_date_converter(value):
        formats = ["%Y-%m-%dT%H:%M:%S"]
        for format in formats:
            try:
                return datetime.datetime.strptime(value, format)
            except Exception:
                pass
        return value

    @staticmethod
    def _date_to_string_converter(value):
        try:
            return value.isoformat()
        except Exception:
            pass
        return value

    @staticmethod
    def _check_for_date_fields(json_item, converter):
        if isinstance(json_item, (dict, list)):
            iterable = json_item.items() if isinstance(json_item, dict) else enumerate(json_item)
            for k, v in iterable:
                if isinstance(v, (dict, list)):
                    BaseView._check_for_date_fields(v, converter)
                else:
                    json_item[k] = converter(v)

    @staticmethod
    def get_response(data, status=HTTPStatus.OK.value):

        BaseView._check_for_date_fields(data, converter=BaseView._date_to_string_converter)
        # TODO: Customise CustomJSONEncoder to handle date
        data = ujson.loads(simplejson.dumps(data, ignore_nan=True, encoding='utf-8', cls=CustomJSONEncoder))

        return response.json(
            {
                'data': data,
                'response_datetime': datetime.datetime.utcnow().isoformat(),
                'status': 'success'
                if (status == HTTPStatus.OK.value or status == HTTPStatus.CREATED.value)
                else 'failed'
            },
            status=status)

    async def options(self, *args, **kwargs):
        headers = {"Access-Control-Allow-Methods": ", ".join(
            [method for method in HTTP_METHODS if hasattr(self, method.lower())])}

        return response.text('', 200, headers=headers)


class BaseDataResource(BaseView):
    def _validate_query(self, args):
        """Validating query params"""
        request_args = self._parse_query(args)
        query_args = MongoIdConverter.id_to_object(request_args)
        return query_args

    def _parse_query(self, args):
        """Validate and load query"""
        query = query_parser.load(args)
        return query.data

    def _parse_data(self, body):
        """Validate data params"""
        data = ujson.loads(body)
        self._check_for_date_fields(data, converter=BaseView._string_to_date_converter)
        MongoIdConverter.to_object_id(data)
        return data

    @staticmethod
    def _get_params(args):
        query = args.get('query')
        projection = args.get('projection')
        return {'query': query, 'projection': projection}

    @abstractmethod
    async def get(self, request: sanic.request, client: str, collection: str) -> sanic.response:
        pass

    @abstractmethod
    async def post(self, request: sanic.request, client: str, collection: str) -> sanic.response:
        pass

    @abstractmethod
    async def put(self, request: sanic.request, client: str, collection: str) -> sanic.response:
        pass

    @abstractmethod
    async def delete(self, request: sanic.request, client: str, collection: str) -> sanic.response:
        pass

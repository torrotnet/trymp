from marshmallow import Schema, fields

from service_api.services.logger import logger
from service_api.exceptions import ApplicationError
import ujson


class ValidationError(ApplicationError):
    pass


class BaseForm(Schema):

    def handle_error(self, exc, data):
        """Log and raise our custom exception when (de)serialization fails."""
        logger.error(exc.messages)
        raise ValidationError(exc, status_code=422)


class RESTQueryParser(BaseForm):
    """Implements a scheme for dumping, loading and validation parameters of the request"""

    query = fields.Method(deserialize='deserialize_query')
    projection = fields.Method(deserialize='deserialize_query')
    bulk_request = fields.Boolean()
    get_last = fields.Boolean()

    def deserialize_query(self, obj):
        query_dict = ujson.loads(obj)
        if not isinstance(query_dict, dict):
            raise TypeError("query instance must be a dict")
        return query_dict


query_parser = RESTQueryParser()

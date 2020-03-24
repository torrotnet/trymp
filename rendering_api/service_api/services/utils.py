from bson import ObjectId


class MongoIdConverter:

    @staticmethod
    def to_object_id(data):
        """Converts all occurrences of 'id' and '_id' from 'str' to 'bson.ObjectId' data type."""
        if isinstance(data, (list, dict)):
            iterable = data.items() if isinstance(data, dict) else enumerate(data)
            for key, value in iterable:
                if isinstance(value, (list, dict)):
                    MongoIdConverter.to_object_id(value)
                if key in ("id", "_id"):
                    data[key] = ObjectId(value)

    @staticmethod
    def id_to_string(data):

        if isinstance(data, list):
            for rec in data:
                MongoIdConverter.__to_string(rec)

        if isinstance(data, dict):
            MongoIdConverter.__to_string(data)

        if isinstance(data, ObjectId):
            data = {'_id': data}
            MongoIdConverter.__to_string(data)

        return data

    @staticmethod
    def id_to_object(request):

        if 'id' in request.get('query', {}) and isinstance(request.get('query', {}).get('id'), str):
            request['query']['_id'] = ObjectId(request['query']['id'])
            del request['query']['id']

        if '_id' in request.get('query', {}) and isinstance(request.get('query', {}).get('_id'), dict):
            for k, v in request.get('query').get('_id').items():
                if isinstance(v, list):
                    new_list = []
                    for object_id in v:
                        new_list.append(ObjectId(object_id))
                    request['query']['_id'][k] = new_list

        return request

    @classmethod
    def __to_string(cls, record):

        if '_id' in record:
            record['id'] = str(record['_id'])
            del record['_id']

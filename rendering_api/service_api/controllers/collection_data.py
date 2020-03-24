from bson.objectid import ObjectId

from service_api.constants import PAGINATE, IGNORED_DBS
from service_api.controllers import AbstractController
from service_api.services.utils import MongoIdConverter


class BaseDataResourceController(AbstractController):
    """Provides a basic interface for accessing the resource"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DataResourceController(BaseDataResourceController):

    async def get_one(self, mongo_id):
        """Get one document from MongoDB by id.

        Args:
            mongo_id (str): Document id.

        Returns:
            Dict with document found:
                {'id': '5c4ee1aba7e63a047e289077', ...}

        """
        mongo_response = await self.app.connect.find_one(ObjectId(mongo_id))
        response = MongoIdConverter.id_to_string(mongo_response)

        if not response:
            response = {}

        return response

    async def create(self, update_params):
        """Create document in MongoDB.

        Args:
            update_params (dict): Dict with new document data.

        Returns:
            Dict with created document:
                {"id": "5c4ee1aba7e63a047e289077", ...}

        """
        connect = self.app.connect
        mongo_response = await connect.insert_one(update_params)
        created_resource = await connect.find_one(ObjectId(mongo_response.inserted_id))
        response = MongoIdConverter.id_to_string(created_resource)

        return response

    async def create_many(self, data):
        mongo_response = await self.app.connect.insert_many(data)
        created_resource = self.app.connect.find({"_id": {"$in": [ObjectId(_id) for _id in mongo_response.inserted_ids]}})
        response = [MongoIdConverter.id_to_string(item) for item in await created_resource.to_list(10000)]
        return response

    async def get_many(self, query, projection=None):
        """Get all documents related to the params argument.

        Args:
            query (Dict): MongoDB query parameters.
            projection (Dict): MongoDB list of field names that should be returned in the result document

        Returns:
            List with documents related to the params:
                [
                    {"id": "5c4ee1aba7e63a047e289077", ...},
                    ...
                    {"id": "5c4ee1aba7e63a047e28907n", ...}
                ]

        """

        sort_by = query.pop("sort", None)

        mongo_response = self.app.connect.find(query, projection)
        if sort_by:
            sort_by = [(key, value) for key, value in sort_by.items()]
            mongo_response = mongo_response.sort(sort_by)
        response = MongoIdConverter.id_to_string(await mongo_response.to_list(PAGINATE))

        return response

    async def update(self, query, data):
        """Update MongoDB document.

        Args:
            query (dict): Update document query.
            data (dict): Update data.

        Returns:
            Boolean update operation status:
                True or False

        """
        mongo_response = await self.app.connect.update_one(query, {'$set': data})
        is_updated = mongo_response.raw_result.get('updatedExisting')
        return is_updated

    async def delete(self, query, bulk):
        """Delete MongoDB document/s.

        Args:
            query (dict): Delete document/s query.
            bulk (bool): Boolean parameter to determine whether
                to delete one document or many.

        Returns:
            Boolean delete operations status:
                True or False

        """
        if bulk:
            mongo_response = await self.app.connect.delete_many(query)
        else:
            mongo_response = await self.app.connect.delete_one(query)

        is_deleted = bool(mongo_response.deleted_count)

        return is_deleted

    async def get_all(self, params, collection):
        """Get all documents that match the parameters.

        Args:
            params (dict): MongoDB query parameters.
            collection (str): Collection name.

        Returns:
            List with documents related to the params:
                [
                    {"id": "5c4ee1aba7e63a047e289077", ...},
                    ...
                    {"id": "5c4ee1aba7e63a047e28907n", ...}
                ]

        """
        mongo_client = self.app.mongo_client

        data = []
        async for db in await mongo_client.list_databases():
            db_name = db.get('name')
            if not db_name or db_name in IGNORED_DBS:
                continue
            mongo_response = await mongo_client[db_name][collection].find(
                params).to_list(PAGINATE)
            response = MongoIdConverter.id_to_string(mongo_response)
            data.extend(response)
        return data

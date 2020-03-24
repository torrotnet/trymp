from sanic_swagger import doc


class Query(doc.Model):
    name = 'query'


class Bulk(doc.Model):
    name = 'bulk_request'
    bulk_request: bool = doc.field()

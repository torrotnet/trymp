from collections import namedtuple


class AbstractController:
    """Abstract Controller for managing data from repositories and business logic

    Args:
        repositories (namedtuple): Namedtuple containing repositories
        call_wrapper (contextmanager): contextmanager for wrapping external
            calls to repositories or other services through http clients
             with boilerplate error checking code
    """
    def __init__(self, app):
        self.app = app


def setup_controllers(app):
    from service_api.controllers.collection_data import DataResourceController

    controllers = namedtuple(
        'controllers',
        ['CollectionDataController']
    )
    app.controllers = controllers(
        DataResourceController(app)
    )

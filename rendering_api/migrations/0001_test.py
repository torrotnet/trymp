from service_api.app import logger
from service_api.migrations.repository import (
    Test,
)


log = logger.get_logger(__name__)
MIGRATION_NAME = __name__.split('.')[-1]

async def migrate(db):
    """Migration engagement_mandatory_information.

    Populates the `common.Metadata` with Global Attributes for Mandatory Questions.
    """
    try:
        test = Test(value='testValue', label='Test label')
        await test.save_to_db(db)
    except Exception as exc:
        log.error(f"Migration {MIGRATION_NAME} has failed")
    else:
        db.Migrations.insert_one({MIGRATION_NAME: True})

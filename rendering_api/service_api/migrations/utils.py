import importlib
import os

from service_api.app import db_client
from service_api.app import logger
from service_api.migrations.repository import TestConfig


log = logger.get_logger(__name__)

mongo_ip, mongo_port = 'mongodb', '27017'
mongo_client = db_client("mongodb://{ip}:{port}/".format(ip=mongo_ip, port=mongo_port))
db = mongo_client.common


def get_all_migrations():
    return sorted([i[:-3] for i in os.listdir('app/migrations') if not i.startswith("_")])


async def check_migration(migration):
    """Check if migration is migrated."""
    try:
        count = await db.Migrations.count_documents({migration: True})
    except Exception as e:
        print(e)
    return count > 0


async def migrate_all():
    for migration_name in get_all_migrations():
        if not await check_migration(migration_name):
            migration = importlib.import_module(f'migrations.{migration_name}')
            if hasattr(migration, 'migrate'):
                await migration.migrate(db)
            else:
                configs = getattr(migration, 'configs', {})
                migration_name = getattr(migration, 'MIGRATION_NAME', None)
                await _migrate(db, configs, migration_name)

            log.info(f'Migration {migration_name} has successfully finished')


async def migrate(migration_name):
    if await check_migration(migration_name):
        log.info(f'{migration_name} is already migrated')
    else:
        migration = importlib.import_module(f'migrations.{migration_name}')
        await migration.migrate(db)


async def _migrate(db, configs, migration_name):
    """Populates the `common.Metadata` with Global Attributes."""
    for test_config in configs:
        try:
            await TestConfig(**test_config).save_to_db(db)
        except Exception as exc:
            log.error(f"Migration {migration_name} has failed")
    else:
        db.Migrations.insert_one({migration_name: True})

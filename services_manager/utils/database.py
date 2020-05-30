import typing as t

from aiohttp.web import Application
from tortoise import Tortoise

from services_manager.settings import SQLITE_PATH
from services_manager.utils.logger import logger


async def init_db(app: Application) -> t.AsyncGenerator:
    models = ['services_manager.models.service_model']
    logger.debug(f'models directory is: {models}')

    logger.debug('ORM initialization')
    await Tortoise.init(
        db_url=f'sqlite://{SQLITE_PATH}', modules={'models': models}
    )
    logger.info('ORM initialization is done')

    logger.debug('DB schemas generation')
    await Tortoise.generate_schemas()
    logger.info('DB schemas generated')

    yield  # AIOHTTP context feature

    logger.warning('closing connections with DB')
    await Tortoise.close_connections()
    logger.info('DB connections is closed')

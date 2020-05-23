import asyncio

import uvloop
from aiohttp import web

from services_manager.utils.logger import logger
from services_manager.settings import APP_DEBUG_MODE

asyncio.set_event_loop(uvloop.new_event_loop())
loop = asyncio.get_event_loop()
logger.debug(f'has set "uvloop" event-loop: {loop}')


def create_app() -> web.Application:
    logger.debug('creating application instance')

    return web.Application(debug=APP_DEBUG_MODE, loop=loop)

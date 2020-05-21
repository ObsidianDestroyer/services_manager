import uvloop
import asyncio

from aiohttp import web

from services_manager.utils.logger import logger


asyncio.set_event_loop(uvloop.new_event_loop())
loop = asyncio.get_event_loop()


def create_app() -> web.Application:
    logger.debug('creating application instance', loop=loop)

    return web.Application(debug=True, loop=loop)


app = create_app()

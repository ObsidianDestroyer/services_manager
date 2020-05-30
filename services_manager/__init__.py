import asyncio
import os.path

import aiohttp_jinja2
import jinja2
import uvloop
from aiohttp import web

from services_manager.routes import (
    front_routes,
    get_available_services,
    guarded_service_actons,
)
from services_manager.settings import APP_DEBUG_MODE
from services_manager.setup.create_services import pre_create_services
from services_manager.utils.database import init_db
from services_manager.utils.logger import logger

asyncio.set_event_loop(uvloop.new_event_loop())
loop = asyncio.get_event_loop()
logger.debug(f'has set "uvloop" event-loop: {loop}')


def create_app() -> web.Application:
    logger.debug('creating application instance')
    app = web.Application(debug=APP_DEBUG_MODE, loop=loop)
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(os.path.join(os.getcwd(), 'templates')),
    )

    app.add_routes(front_routes)
    app.add_routes(
        [
            web.get('/api/services', get_available_services),
            web.post('/api/services', guarded_service_actons),
        ]
    )

    app.cleanup_ctx.append(init_db)
    app.cleanup_ctx.append(pre_create_services)
    return app

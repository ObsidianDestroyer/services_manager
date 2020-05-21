from aiohttp import web

from services_manager import create_app

web.run_app(create_app(), port=2731)

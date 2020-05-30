import os

from aiohttp import web

from services_manager import create_app

if os.getuid() == 0:
    web.run_app(create_app(), port=2731)
else:
    raise PermissionError('you are must run this application as root')

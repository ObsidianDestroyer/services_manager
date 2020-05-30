import aiohttp_jinja2
from aiohttp import web

from services_manager.utils.logger import logger

front_routes = web.RouteTableDef()


@front_routes.get('/')
@aiohttp_jinja2.template('index.jinja2')
def index_page(request: web.Request) -> dict:
    logger.debug(
        f'incoming request [{request.method}] {request.url} : {request.host}'
    )
    response = {'services': []}
    for key in request.app.keys():
        if 'service_' in key:
            service: dict = request.app[key].model.render()
            service['actions'] = {
                'start': (
                    '/api/services?serviceName='
                    f'{service["serviceName"]}&action=start'
                ),
                'stop': (
                    '/api/services?serviceName='
                    f'{service["serviceName"]}&action=stop'
                ),
                'restart': (
                    f'/api/services?serviceName='
                    f'{service["serviceName"]}&action=restart'
                ),
            }
            response['services'].append(service)
    return response

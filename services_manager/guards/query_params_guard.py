from aiohttp import web

from services_manager.utils.logger import logger


async def services_query_params_guard(request: web.Request) -> web.Response:
    query = dict(request.query)
    available_keys = ['serviceName', 'action']
    for a_key, q_key in zip(available_keys, query):
        if a_key == q_key:
            key = query.get(a_key)
            if key:
                continue
            else:
                logger.error('bad query params, request aborted')
                return web.json_response(
                    {'error': 'bad query params'}, status=400
                )
    request.query_payload = query
    return request

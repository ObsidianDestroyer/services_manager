import typing as t

from aiohttp import web

from services_manager.guards.apply_guards import apply_guards
from services_manager.guards.query_params_guard import (
    services_query_params_guard,
)
from services_manager.routes.api_helpers.apply_action import (
    apply_service_action,
)
from services_manager.utils.logger import logger


async def get_available_services(request: web.Request) -> web.Response:
    logger.debug(
        f'incoming request [{request.method}] {request.url} : {request.host}'
    )
    response: t.List[dict] = []
    for key in request.app.keys():
        if 'service_' in key:
            service = request.app[key]
            response.append(service.model.render())

    return web.json_response(response, status=200)


# FIXME: Make a query params guard here ! ! !
async def action_with_service(request: web.Request) -> web.Response:
    logger.debug(
        f'incoming request [{request.method}] {request.url} : {request.host}'
    )
    service = request.app[f'service_{request.query_payload["serviceName"]}']
    try:
        action = request.query_payload['action']
        response: dict = await apply_service_action(service, action)
        print(response)
        return web.json_response(response, status=200)

    except RuntimeError:
        response = service.model.render()
        response['error'] = 'application already running'
        return web.json_response(response, status=303)

    except ValueError:
        response = service.model.render()
        response['error'] = 'failed to stop service due an error'
        return web.json_response(response, status=500)

    except AttributeError:
        response = service.model.render()
        response['error'] = 'failed to restart service due an error'
        return web.json_response(response, status=500)

    except KeyError:
        return web.json_response(
            {'error': f'bad action \'{request.query_payload["action"]}\''},
            status=400,
        )


guarded_service_actons = apply_guards(
    action_with_service, services_query_params_guard
)

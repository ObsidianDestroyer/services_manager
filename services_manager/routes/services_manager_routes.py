from aiohttp import web

api_routes = web.RouteTableDef()


@api_routes.get('/api/services')
async def get_available_services(request: web.Request) -> web.Response:
    pass

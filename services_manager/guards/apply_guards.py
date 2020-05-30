import typing as t

from aiohttp.web import Response


def apply_guards(route, *guards) -> t.Callable:
    async def wrapper(request) -> Response:
        result = request
        for guard in guards:
            result = await guard(result)
            if isinstance(result, Response):
                return result
        return await route(result)

    return wrapper

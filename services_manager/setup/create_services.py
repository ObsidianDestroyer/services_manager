import typing as t

from aiohttp.web import Application

from services_manager.core.services import SSHDservice, VSFTPDService
from services_manager.models import Service
from services_manager.utils.logger import logger


async def pre_create_services(app: Application) -> None:
    logger.debug('pre-creating services DB records')
    services: t.List[dict] = [
        {'name': 'vsftpd', 'status': False, 'service_obj': VSFTPDService},
        {'name': 'sshd', 'status': False, 'service_obj': SSHDservice},
    ]
    for service in services:
        service_cls = service['service_obj']
        status: bool = service['status']
        name: str = service['name']
        exist_service: Service = await Service.filter(name=name).first()
        if not exist_service:
            logger.debug(f'creating DB record for {name!r}')
            new_service = await Service.create(name=name, status=status)
            service_obj = service_cls(new_service)

            app[f'service_{name}'] = service_obj
            logger.info(f'pre-created service {name!r}')
        else:
            logger.warning(f'service {name!r} DB record exists')
            service_obj = service_cls(exist_service)

            app[f'service_{name}'] = service_obj
            logger.info(f're-created instance of service {name!r}')
            # AIOHTTP context is async, so 'continue' need to lock it
            continue
    yield

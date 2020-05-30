from services_manager.core.structures import ServiceDaemon
from services_manager.utils.logger import logger


async def apply_service_action(service: ServiceDaemon, action: str) -> dict:
    if action == 'start':
        logger.debug(f'incoming request to {action} service: {service}')
        await service.run_service(with_systemctl=True)
        return service.model.render()

    elif action == 'stop':
        logger.debug(f'incoming request to {action} service: {service}')
        await service.stop_service()
        return service.model.render()

    elif action == 'restart':
        logger.debug(f'incoming request to {action} service: {service}')
        await service.restart_service()
        return service.model.render()
    else:
        logger.warning(f'incoming request to {action} service: {service}')
        logger.error(f'not available action {action}')
        raise KeyError

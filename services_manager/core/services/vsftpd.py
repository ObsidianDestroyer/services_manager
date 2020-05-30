from services_manager.core.structures import ServiceDaemon
from services_manager.models import Service


class VSFTPDService(ServiceDaemon):
    def __init__(self, service_model: Service, service_args=None) -> None:
        super().__init__(service_model, service_args=service_args)

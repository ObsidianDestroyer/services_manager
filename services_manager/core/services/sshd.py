from services_manager.core.structures import ServiceDaemon


class SSHDservice(ServiceDaemon):
    def __init__(self, service_name, service_args=None) -> None:
        super().__init__(service_name, service_args=service_args)

import asyncio
import subprocess
import sys
import typing as t

from services_manager.models import Service
from services_manager.utils.logger import logger


class ServiceDaemon:
    def __init__(
        self, service_model: Service, service_args: t.List[str] = None,
    ) -> None:
        self.name: str = service_model.name
        self.model: Service = service_model
        self.service_args: t.List[str] = service_args
        self.pid: int = None
        self.state: bool = False
        self.locked: bool = True
        self._process: subprocess.Popen = None
        self._loop = asyncio.get_running_loop()
        self._task: asyncio.Task = None
        self._systemctl: bool = False
        self._sync_service_states()

    def _sync_service_states(self) -> None:
        if self.model.status != self.state:
            self.model.status = False
            asyncio.gather(self.model.save())
            logger.debug('synchronized')

    def _check_exit_code(self, process: subprocess.Popen) -> int:
        while process.poll() is None:
            continue
        else:
            if process.poll() == 0:
                self.pid = process.pid
                logger.info(f'process {self.name!r} started; PID={self.pid}')
                self.state = True
                self.locked = False
                return process, process.poll()
            else:
                self.state = False
                self.locked = True
                return process, process.poll()

    def _exec_command(self, with_systemctl=False) -> subprocess.Popen:
        logger.debug(f'invoked service: {self.name}')
        self._systemctl: bool = with_systemctl
        if not self.service_args:
            process = subprocess.Popen(
                (
                    [self.name]
                    if not with_systemctl
                    else ['systemctl', 'start', f'{self.name}']
                ),
                stdout=sys.stdout,
            )
            return self._check_exit_code(process)
        else:
            process = subprocess.Popen(
                [self.name, *self.service_args], stdout=sys.stdout
            )
            return self._check_exit_code(process)

    async def run_service(self, with_systemctl=False) -> None:
        self._process, return_code = self._exec_command(
            with_systemctl=with_systemctl
        )

        if return_code == 0:
            # if "returncode" is None \
            #   it means process is running and not exited yet
            logger.debug(
                f'service {self.name!r} running; exit_code={return_code}'
            )
            self.model.status = self.state
            self.model.locked = self.locked
            await self.model.save()
        else:
            logger.error(
                f'failed to start service: {self.name!r}; '
                f'exit_code={self._process.returncode}'
            )
            raise RuntimeError

    async def stop_service(self) -> None:
        if self.state is True and self._process is not None:
            logger.debug(f'killing process {self.name!r}; PID={self.pid}')
            self.state = False
            self.locked = False

            try:
                if not self._systemctl:
                    self._process.kill()
                    logger.warning(
                        f'process \'{self.name}:{self.pid}\' killed'
                    )
                else:
                    subprocess.Popen(['systemctl', 'stop', f'{self.name}'])

                self.model.locked = self.locked
                self.model.status = self.state
                await self.model.save()

            except Exception as err:
                logger.error(
                    f'failed to stop service: {self.name}; PID={self.pid}'
                )
                self.model.locked = True
                await self.model.save()
                raise err
        else:
            logger.debug(
                f'attempt to kill process {self.name}; process={self._process}'
            )
            raise ValueError

    async def restart_service(self) -> None:
        # May be extended with systemctl application for "soft" restart
        if self.state is True and not self.locked:
            logger.warning(f'restarting service {self.name!r}')
            await self.stop_service()

            logger.debug(f'timeout before service {self.name!r} re-run')
            await asyncio.sleep(5)

            await self.run_service(with_systemctl=self._systemctl)

        elif self.locked:
            logger.error(
                f'cant restart {self.name!r} '
                'service due it\'s LOCKED for using'
            )
            raise ValueError
        else:
            logger.error('failed to restart service ' f'{self.name!r}')
            raise AttributeError

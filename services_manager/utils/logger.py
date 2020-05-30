import logging
import logging.config
import logging.handlers
import sys
import syslog

from services_manager.settings import LOGFILE_PATH

__all__ = ['logger']


def create_logger() -> logging.Logger:
    logging.config.dictConfig(
        {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'verbose': {
                    'format': (
                        '[%(asctime)s] line: %(name)s-%(lineno)-6s%'
                        '(levelname)-6s %(message)s'
                    )
                }
            },
            'handlers': {
                'stdout': {
                    'class': 'logging.StreamHandler',
                    'stream': sys.stdout,
                    'formatter': 'verbose',
                    'level': logging.NOTSET,  # FIXME: Change to INFO
                },
                'sys-app-logger': {
                    'class': 'logging.handlers.SysLogHandler',
                    'address': '/dev/log',
                    'level': logging.NOTSET,  # FIXME: Change to DEBUG
                    'facility': syslog.LOG_USER,
                    'formatter': 'verbose',
                },
                'app-file-handler': {
                    'class': 'logging.FileHandler',
                    'filename': LOGFILE_PATH,
                    'formatter': 'verbose',
                    'level': logging.NOTSET,
                },
            },
            'loggers': {
                'main': {
                    'handlers': [
                        'sys-app-logger',
                        'stdout',
                        'app-file-handler',
                    ],
                    'level': logging.DEBUG,
                    'propagate': True,
                }
            },
        }
    )
    logger_ = logging.getLogger('main')
    return logger_


logger = create_logger()

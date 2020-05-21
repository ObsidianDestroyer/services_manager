import logging
import structlog

__all__ = ['logger']


def create_logger() -> structlog.PrintLogger:
    logging.basicConfig(level=logging.NOTSET)
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.TimeStamper(),
            structlog.dev.ConsoleRenderer(colors=True, force_colors=True),
            structlog.dev.set_exc_info,
        ],
        wrapper_class=structlog.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=False,
    )
    return structlog.get_logger()


logger = create_logger()

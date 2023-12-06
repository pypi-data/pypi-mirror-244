import logging.config
import structlog
import os
import pathlib
from structlog.contextvars import (
    bind_contextvars,
    clear_contextvars,
    merge_contextvars,
    unbind_contextvars,
)


LOG_LEVEL = os.getenv("STONEWAVE_LOG_LEVEL") or "INFO"
LOG_LEVEL = str(LOG_LEVEL).upper()
LOG_LEVEL = "DEBUG" if LOG_LEVEL == "TRACE" else LOG_LEVEL
timestamper = structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S")
log_file_dir = os.path.join(os.getenv("STONEWAVE_HOME", "/tmp"), "logs", "py_table_funcs")
pathlib.Path(log_file_dir).mkdir(parents=True, exist_ok=True)


def get_logger(logger_id=None):
    if not os.path.exists(log_file_dir):
        os.mkdir(log_file_dir)
    if logger_id is None:
        logger_config = get_logger_config()
    else:
        log_file = os.path.join(log_file_dir, "py_table_funcs.{}.log".format(logger_id))
        logger_config = get_logger_config(log_file)
    logging.config.dictConfig(logger_config)
    structlog.configure(
        processors=[
            merge_contextvars,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            timestamper,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    logger = structlog.get_logger()
    bind_contextvars(pid=os.getpid())
    return logger


def get_logger_config(log_file=os.path.join(log_file_dir, "py_table_funcs.{}.log".format(os.getpid() % 1000))):
    pre_chain = [
        # Add the log level and a timestamp to the event_dict if the log entry
        # is not from structlog.
        structlog.stdlib.add_log_level,
        timestamper,
    ]

    logger_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "plain": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.dev.ConsoleRenderer(colors=False),
                "foreign_pre_chain": pre_chain,
            },
        },
        "handlers": {
            "file": {
                "level": LOG_LEVEL,
                "class": "logging.handlers.RotatingFileHandler",
                "filename": log_file,
                "formatter": "plain",
                "maxBytes": 2097152,  # 2MB
                "backupCount": 1,
            },
        },
        "loggers": {
            "": {
                "handlers": ["file"],
                "level": LOG_LEVEL,
                "propagate": True,
            },
        },
    }
    return logger_config


logger = get_logger()

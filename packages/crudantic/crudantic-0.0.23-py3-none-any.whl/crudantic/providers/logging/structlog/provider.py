import os
from typing import Any
import logging
import structlog
import orjson

LOG_LEVEL_MAP = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
}
LOG_LEVEL_DEFAULT = "info"
LOG_LEVEL = LOG_LEVEL_MAP[os.getenv("LOG_LEVEL", LOG_LEVEL_DEFAULT).upper()]
LOG_AS_JSON = os.getenv("LOG_AS_JSON", "false").upper() == "TRUE"
LOG_PROCESSORS = [
    structlog.contextvars.merge_contextvars,
    structlog.processors.add_log_level,
    structlog.processors.StackInfoRenderer(),
    structlog.dev.set_exc_info,
    structlog.processors.TimeStamper(fmt="iso", utc=True),
    structlog.processors.CallsiteParameterAdder(
        parameters=[
            structlog.processors.CallsiteParameter.FUNC_NAME,
            structlog.processors.CallsiteParameter.PATHNAME,
            structlog.processors.CallsiteParameter.LINENO,
        ]
    ),
]


def reduce_log_line_length(logger, method_name, event_dict):
    if "func_name" in event_dict:
        event_dict["func"] = event_dict["func_name"]
        del event_dict["func_name"]
    if "lineno" in event_dict:
        event_dict["line"] = event_dict["lineno"]
        del event_dict["lineno"]
    if "pathname" in event_dict:
        event_dict["path"] = event_dict["pathname"]
        del event_dict["pathname"]
    return event_dict


LOG_PROCESSORS.append(reduce_log_line_length)

if LOG_AS_JSON:
    LOG_PROCESSORS.append(structlog.processors.JSONRenderer(serializer=orjson.dumps))  # type: ignore
else:
    LOG_PROCESSORS.append(structlog.dev.ConsoleRenderer(colors=True))  # type: ignore

structlog.configure(
    processors=LOG_PROCESSORS,
    wrapper_class=structlog.make_filtering_bound_logger(LOG_LEVEL),
    context_class=dict,
    logger_factory=structlog.BytesLoggerFactory()
    if LOG_AS_JSON
    else structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=True,
)


def get_logger(name: str):
    logger = structlog.get_logger(name)
    return logger

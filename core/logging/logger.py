import json
import sys
from pprint import pformat

import pytz
import stackprinter
from loguru import logger
from loguru._defaults import LOGURU_FORMAT

import logging


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


def format_record(record: dict) -> str:
    format_string = LOGURU_FORMAT
    if record["extra"].get("payload") is not None:
        record["extra"]["payload"] = pformat(
            record["extra"]["payload"],
            indent=4,
            compact=True,
            width=88,
        )
        format_string += "\n<level>{extra[payload]}</level>"

    format_string += "{exception}\n"
    return format_string


def init_logging():
    loggers = (
        logging.getLogger(name)
        for name in logging.root.manager.loggerDict
        if name.startswith("uvicorn.")
    )
    for uvicorn_logger in loggers:
        uvicorn_logger.handlers = []

    intercept_handler = InterceptHandler()
    logging.getLogger("uvicorn").handlers = [intercept_handler]

    def sink_serializer(message):
        record = message.record
        timestamp = record["time"].astimezone(pytz.utc)
        timestamp = timestamp.strftime("%Y-%m-%dT%H:%M:%S.{:03d}Z").format(
            timestamp.microsecond // 1000
        )

        try:
            msg = json.loads(record["message"])
        except:
            msg = record["message"]

        serializable = {
            "@timestamp": timestamp,
            "icon": record["level"].icon,
            "log": {"level": record["level"].name},
            "function": record["function"],
            "file": {
                "file": record["file"].name,
                "name": record["name"],
                "line": record["line"],
            },
            "message": msg,
        }
        if record["exception"]:
            exc_class = record["exception"].type
            serializable = {
                **serializable,
                "exc": {
                    "type": f"{exc_class.__module__}.{exc_class.__name__}",
                    "value": record["exception"].value,
                    "traceback": stackprinter.format(
                        record["exception"], show_vals="line"
                    ),
                },
            }
        serialized = json.dumps(serializable)
        print(serialized, file=sys.stdout, flush=True)

    # logger.configure(
    #     #     handlers=[
    #     #         {
    #     #             "sink": True,
    #     #             "format": "{level}: {time} [{name}] {message}",
    #     #         }
    #     #     ]
    #     # )
    logger.configure(
        handlers=[{"sink": sys.stdout, "level": logging.DEBUG, "format": format_record}]
    )

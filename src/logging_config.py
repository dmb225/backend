import logging
import logging.config
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "app.log")


def setup_logging() -> None:
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(name)s: %(message)s",
            },
            "json": {
                "format": '{"time": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s"}',  # noqa: E501
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": LOG_LEVEL,
            },
            "file": {
                "class": "logging.FileHandler",
                "filename": LOG_FILE,
                "formatter": "default",
                "level": LOG_LEVEL,
            },
            "http": {
                "class": "logging.handlers.HTTPHandler",
                "host": os.getenv("LOG_REMOTE_HOST", "localhost:8000"),
                "url": os.getenv("LOG_REMOTE_URL", "/log"),
                "method": "POST",
                "formatter": "json",
                "level": "ERROR",
            },
        },
        "root": {
            "handlers": ["console", "file", "http"],
            "level": LOG_LEVEL,
        },
        "loggers": {
            "watchfiles.main": {
                "level": "WARNING",
                "handlers": ["console", "file", "http"],
                "propagate": False,
            }
        },
    }

    logging.config.dictConfig(logging_config)

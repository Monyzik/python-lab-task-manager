import logging.config

from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent.parent

LOGGING_CONFIG = {
    "version": 1,
    "formatters": {
        "standard": {
            "format": "[%(levelname)s]: %(message)s",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "standard",
            "level": "DEBUG",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "mode": "a",
            "filename": f"{PROJECT_DIR}/.log",
            "level": "DEBUG",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
        }
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

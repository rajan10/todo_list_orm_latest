from decouple import config
from logging.config import dictConfig

DATABASE_URI = config("database_uri", default="localhost")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "file": {
            "format": "%(asctime)s: %(levelname)s: %(module)s: %(funcName)s: %(lineno)d: %(message)s"
        },
    },
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "formatter": "file",
            "filename": "todo.log",
        },
        "stream": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "file",
        },
    },
    "loggers": {
        "": {
            "handlers": ["file"],
            "level": "INFO",
            "propogate": True,
        },
    },
}

dictConfig(LOGGING)

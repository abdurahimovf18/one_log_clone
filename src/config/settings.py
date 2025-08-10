import sys
from datetime import UTC, timezone
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pythonjsonlogger import jsonlogger

from .enums import LogLevel

ROOT: Path = Path(__file__).resolve().parent.parent.parent

LOG_DIR: Path = ROOT / "resources" / "logs"
LOG_DIR.mkdir(exist_ok=True, parents=True)


class Env(BaseSettings):
    #  === Application Settings ===
    DEBUG: bool
    LOG_LEVEL: LogLevel

    #  === Bot Settings ===
    BOT_TOKEN: str

    #  === Database Settings ===
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str

    #  === Redis Settings ===
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str | None = None
    REDIS_DB: int

    model_config = SettingsConfigDict(
        env_file=ROOT / ".env",
    )

    
env = Env()  # type: ignore

DEBUG: bool = env.DEBUG
TIMEZONE: timezone = UTC

# sqlalchemy url: database+driver://{user}:{password}@{host}:{port}/{db_name} 
DATABASE_URL: str = (
    f"postgresql+psycopg://{env.DATABASE_USER}:{env.DATABASE_PASSWORD}"
    f"@{env.DATABASE_HOST}:{env.DATABASE_PORT}/{env.DATABASE_NAME}"
)

if DEBUG:
    LOG_LEVEL: str = LogLevel.DEBUG.value
else:
    LOG_LEVEL: str = env.LOG_LEVEL.value  # type: ignore


LOGGING_CONFIG: dict[str, object] = {
    "version": 1,
    "disable_existing_loggers": False,  # Keep existing loggers (e.g., uvicorn, aiogram)
    "formatters": {
        "plain": {  # human-readable, plain text
            "format": "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%SZ",  # UTC, ISO 8601
        },
        "json": {  # JSON structured logs
            "()": jsonlogger.JsonFormatter,  # type: ignore
            "fmt": "%(asctime)s %(levelname)s %(name)s %(message)s %(filename)s:%(lineno)d",
            "datefmt": "%Y-%m-%dT%H:%M:%SZ",
        },
    },
    "handlers": {
        "console": {  # No colors, for dev/debug
            "class": "logging.StreamHandler",
            "formatter": "plain",
            "stream": sys.stdout,
            "level": LOG_LEVEL,
        },
        "json_file": {  # Rotating JSON log file
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "json",
            "filename": LOG_DIR / "app.json.log",
            "maxBytes": 5 * 1024 * 1024,  # 5 MB
            "backupCount": 5,  # Keep last 5 files
            "encoding": "utf-8",
            "level": LOG_LEVEL,
        },
    },
    "root": {  # Default logger
        "handlers": ["console", "json_file"],
        "level": "DEBUG",
    },
    "loggers": {
        # Example: custom logger with separate level
        "aiogram": {
            "handlers": ["console", "json_file"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn": {
            "handlers": ["console", "json_file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

import sys
from datetime import UTC, timedelta, timezone
from pathlib import Path

from aiogram.utils.i18n import lazy_gettext as __
from pydantic_settings import BaseSettings, SettingsConfigDict
from pythonjsonlogger import json

from .enums import BotCommand, LogLevel, TimeDelta, UserLanguage, UserLanguages

ROOT: Path = Path(__file__).resolve().parent.parent.parent

LOG_DIR: Path = ROOT / "resources" / "logs"
LOG_DIR.mkdir(exist_ok=True, parents=True)

LOCALE_DIR: Path = ROOT / "locales"
LOCALE_DIR.mkdir(exist_ok=True, parents=True)

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
            "()": json.JsonFormatter,  # type: ignore
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
        "level": LOG_LEVEL,
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

# Supported languages for the application.
# To add new languages, update the database schema and manage translations.
# See the Makefile for commands to handle translation updates with pybabel.
LANGUAGES: tuple[UserLanguage, ...] = (
    UserLanguage(code=UserLanguages.EN, flag="🇺🇸"),
    UserLanguage(code=UserLanguages.UZ, flag="🇺🇿"),
    UserLanguage(code=UserLanguages.RU, flag="🇷🇺"),
)

DEFAULT_LANGUAGE: UserLanguages = UserLanguages.EN

#  === Security Settings ===
PASSWORD_HASH_TIME_COST = 3            # Iterations or cost factor
PASSWORD_HASH_MEMORY_COST = 65536      # Memory in KiB (Argon2 / scrypt)
PASSWORD_HASH_PARALLELISM = 2          # Threads / lanes
PASSWORD_HASH_LENGTH = 32              # Output length in bytes
PASSWORD_HASH_SALT_LENGTH = 16         # Salt length in bytes

# === BOT Settings ===
MESSAGE_RATE_PER_SECOND = 30
BOT_THROTTLING_PER_SECOND = 3

BOT_COMMANDS: list[BotCommand] = [
    BotCommand(command="start", description=__("Start or restart the bot")),
    BotCommand(command="help", description=__("Show available commands and usage")),
    BotCommand(command="language", description=__("Switch your preferred language")),
    BotCommand(command="feedback", description=__("Leave Feedback")),
]

# === Model Settings ===
INTERVALS: tuple[TimeDelta, ...] = (
    TimeDelta(
        label=__("30 Minutes"),
        value=timedelta(minutes=30),
        callback_value="30m"
    ),
    TimeDelta(
        label=__("1 Hour"),
        value=timedelta(hours=1),
        callback_value="1h"
    ),
    TimeDelta(
        label=__("1 Hour 30 Minutes"),
        value=timedelta(hours=1, minutes=30),
        callback_value="1h30m"
    ),
    TimeDelta(
        label=__("3 Hours"),
        value=timedelta(hours=3),
        callback_value="3h"
    ),
    TimeDelta(
        label=__("6 Hours"),
        value=timedelta(hours=6),
        callback_value="6h"
    ),
)

DEFAULT_INTERVAL: TimeDelta = INTERVALS[1]
DURATIONS: tuple[TimeDelta, ...] = (
    TimeDelta(
        label=__("3 Hours"),
        value=timedelta(hours=3),
        callback_value="3h"
    ),
    TimeDelta(
        label=__("6 Hours"),
        value=timedelta(hours=6),
        callback_value="6h"
    ),
    TimeDelta(
        label=__("9 Hours"),
        value=timedelta(hours=9),
        callback_value="9h"
    ),
    TimeDelta(
        label=__("12 Hours"),
        value=timedelta(hours=12),
        callback_value="12h"
    ),
    TimeDelta(
        label=__("1 Days"),
        value=timedelta(hours=1),
        callback_value="1d"
    ),
    TimeDelta(
        label=__("3 Days"),
        value=timedelta(hours=3),
        callback_value="3d"
    ),
    TimeDelta(
        label=__("7 Days"),
        value=timedelta(hours=7),
        callback_value="7d"
    ),
    TimeDelta(
        label=__("30 Days"),
        value=timedelta(hours=30),
        callback_value="30d"
    ),
)

DEFAULT_DURATION: TimeDelta = DURATIONS[4]

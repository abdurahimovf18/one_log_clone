from enum import Enum
from typing import NamedTuple


class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class UserLanguages(Enum):
    UZ = "UZ"
    RU = "RU"
    EN = "EN"


class UserLanguage(NamedTuple):
    language: UserLanguages
    display_text: str

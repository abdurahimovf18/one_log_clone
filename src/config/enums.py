from datetime import timedelta
from enum import Enum
from typing import NamedTuple

from babel.support import LazyProxy


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
    code: UserLanguages
    flag: str


class TimeDelta(NamedTuple):
    label: LazyProxy
    value: timedelta
    callback_value: str

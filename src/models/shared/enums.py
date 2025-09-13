from enum import Enum

from src.config.enums import UserLanguages

Languages = UserLanguages


class FeedbackStatus(Enum):
    NEW = "NEW"
    IN_REVIEW = "IN_REVIEW"
    ANSWERED = "ANSWERED"
    CLOSED = "CLOSED"


class MessageStatus(Enum):
    CREATED = "CREATED"
    STARTED = "STARTED"
    FINISHED = "FINISHED"

from typing import Annotated

from pydantic import Field

from src.core.domain_schema.shared_schema import CHAT_ID, CREATED_AT, UPDATED_AT, UUID_ID
from src.models.shared.enums import FeedbackStatus


class Feedback:
    type id = UUID_ID
    type chat_id = CHAT_ID
    type user_id = CHAT_ID
    type reply_message_id = Annotated[int, Field()]

    type status = Annotated[FeedbackStatus, Field()]
    type message = Annotated[str, Field()]
    
    type created_at = CREATED_AT
    type updated_at = UPDATED_AT


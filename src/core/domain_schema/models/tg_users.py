from typing import Annotated

from pydantic import Field

from src.config.settings import DEFAULT_LANGUAGE
from src.core.domain_schema.settings import UserLanguages
from src.core.domain_schema.shared_schema import CHAT_ID, CREATED_AT, UPDATED_AT, UUID_ID


class TgUser:
    type chat_id = CHAT_ID
    type user_id = UUID_ID

    type language = Annotated[UserLanguages, Field(default=DEFAULT_LANGUAGE)]
    
    type created_at = CREATED_AT
    type updated_at = UPDATED_AT
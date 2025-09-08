from typing import Annotated

from pydantic import Field

from src.config.settings import DEFAULT_LANGUAGE
from src.core.domain_schema.settings import UserLanguages
from src.core.domain_schema.shared_schema import UUID_ID, ChatID, CreatedAt, UpdatedAt


class TgUser:
    type chat_id = ChatID
    type user_id = UUID_ID

    type language = Annotated[UserLanguages, Field(default=DEFAULT_LANGUAGE)]
    
    type created_at = CreatedAt
    type updated_at = UpdatedAt
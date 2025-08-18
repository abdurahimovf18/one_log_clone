from pydantic import Field

from src.core.data_transfer_objects.base import BaseDTO
from src.core.domain_schema.models import UserLanguage


class ExistsDTO(BaseDTO):
    chat_id: UserLanguage.chat_id | None = Field(default=None)
    language: UserLanguage.language | None = Field(default=None)
    created_at: UserLanguage.created_at | None = Field(default=None)
    updated_at: UserLanguage.updated_at | None = Field(default=None)


class GetByChatIdDTO(BaseDTO):
    chat_id: UserLanguage.chat_id


class CreateDTO(BaseDTO):
    chat_id: UserLanguage.chat_id
    language: UserLanguage.language


class UpdateDTO(BaseDTO):
    chat_id: UserLanguage.chat_id
    language: UserLanguage.language

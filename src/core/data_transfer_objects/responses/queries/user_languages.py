from src.core.data_transfer_objects.base import BaseDTO
from src.core.domain_schema.models import UserLanguage


class GetByChatIdDTO(BaseDTO):
    language: UserLanguage.language


class CreateDTO(BaseDTO):
    chat_id: UserLanguage.chat_id
    language: UserLanguage.language
    created_at: UserLanguage.created_at
    updated_at: UserLanguage.updated_at


class UpdateDTO(BaseDTO):
    chat_id: UserLanguage.chat_id
    language: UserLanguage.language
    created_at: UserLanguage.created_at
    updated_at: UserLanguage.updated_at

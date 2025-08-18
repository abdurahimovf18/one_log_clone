from src.core.data_transfer_objects.base import BaseDTO
from src.core.domain_schema.models import UserAuth, UserLanguage


class SetUserLanguageDTO(BaseDTO):
    chat_id: UserLanguage.chat_id
    language: UserLanguage.language
    created_at: UserLanguage.created_at
    updated_at: UserLanguage.updated_at


class SignInDTO(BaseDTO):
    user_id: UserAuth.user_id
    chat_id: UserAuth.chat_id

from src.core.data_transfer_objects.base import BaseDTO
from src.core.domain_schema.models import User, UserAuth, UserLanguage


class SetUserLanguageDTO(BaseDTO):
    chat_id: UserLanguage.chat_id
    language: UserLanguage.language


class SignInDTO(BaseDTO):
    username: User.username
    password: User.password
    chat_id: UserAuth.chat_id

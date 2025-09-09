from src.core.data_transfer_objects.base import BaseDTO
from src.core.domain_schema.models import TgUser, UserAuth


class RegisterTgUserDTO(BaseDTO):
    chat_id: TgUser.chat_id
    language: TgUser.language


class SignInDTO(BaseDTO):
    username: UserAuth.username
    password: UserAuth.password
    chat_id: TgUser.chat_id


class SignUpDTO(BaseDTO):
    username: UserAuth.username
    password: UserAuth.password
    
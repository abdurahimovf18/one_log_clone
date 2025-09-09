from src.core.data_transfer_objects.base import BaseDTO
from src.core.domain_schema.models import TgUser


class RegisterTgUserDTO(BaseDTO):
    chat_id: TgUser.chat_id
    language: TgUser.language

from src.core.data_transfer_objects.base import BaseDTO
from src.core.domain_schema.models import TgUser


class RegisterTgUserDTO(BaseDTO):
    chat_id: TgUser.chat_id
    user_id: TgUser.user_id

    language: TgUser.language
    
    created_at: TgUser.created_at
    updated_at: TgUser.updated_at

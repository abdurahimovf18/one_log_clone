from src.core.data_transfer_objects.base import BaseDTO
from src.core.domain_schema.models import TgUser


class GetByChatIdDTO(BaseDTO):
    language: TgUser.language


class GetUserIdByChatIdDTO(BaseDTO):
    user_id: TgUser.user_id | None


class CreateDTO(BaseDTO):
    chat_id: TgUser.chat_id
    language: TgUser.language
    created_at: TgUser.created_at
    updated_at: TgUser.updated_at


class UpdateDTO(BaseDTO):
    chat_id: TgUser.chat_id
    language: TgUser.language
    created_at: TgUser.created_at
    updated_at: TgUser.updated_at


class SetUserIdByChatId(BaseDTO): ...
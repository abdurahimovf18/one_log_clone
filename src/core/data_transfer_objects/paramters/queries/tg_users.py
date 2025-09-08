from src.core.data_transfer_objects.base import BaseDTO
from src.core.domain_schema.models import TgUser


class ExistsByChatIdDTO(BaseDTO):
    chat_id: TgUser.chat_id


class GetByChatIdDTO(BaseDTO):
    chat_id: TgUser.chat_id


class GetUserIdByChatIdDTO(BaseDTO):
    chat_id: TgUser.chat_id


class CreateDTO(BaseDTO):
    chat_id: TgUser.chat_id
    language: TgUser.language


class UpdateDTO(BaseDTO):
    chat_id: TgUser.chat_id
    language: TgUser.language

from src.core.data_transfer_objects.base import BaseDTO
from src.core.domain_schema.models import (
    Feedback, TgUser, UserAuth, Message
)
from src.models.shared.enums import FeedbackStatus


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
    

class AcceptFeedbackDTO(BaseDTO):
    chat_id: Feedback.chat_id
    user_id: Feedback.user_id
    reply_message_id: Feedback.reply_message_id

    status: Feedback.status = FeedbackStatus.NEW
    message: Feedback.message


class GetCurrentMessageDTO(BaseDTO):
    user_id: Message.owner_id

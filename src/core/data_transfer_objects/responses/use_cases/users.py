from src.core.data_transfer_objects.base import BaseDTO
from src.core.domain_schema.models import Feedback, Message, TgUser, UserAuth


class RegisterTgUserDTO(BaseDTO):
    chat_id: TgUser.chat_id
    user_id: TgUser.user_id

    language: TgUser.language
    
    created_at: TgUser.created_at
    updated_at: TgUser.updated_at


class SignInDTO(BaseDTO):
    pass


class SignUpDTO(BaseDTO):
    username: UserAuth.username
    password: UserAuth.password
    created_at: UserAuth.created_at


class AcceptFeedbackDTO(BaseDTO):
    id: Feedback.id
    status: Feedback.status


class GetCurrentMessageDTO(BaseDTO):
    id: Message.id
    text_id: Message.text_id | None = None
    owner_id: Message.owner_id
    interval: Message.interval
    duration: Message.duration


class UpdateMessageTextDTO(BaseDTO):
    text: Message.text_id
    
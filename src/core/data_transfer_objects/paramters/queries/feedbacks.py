from src.core.data_transfer_objects.base import BaseDTO
from src.core.domain_schema.models import Feedback


class CreateDTO(BaseDTO): 
    chat_id: Feedback.chat_id
    user_id: Feedback.user_id
    reply_message_id: Feedback.reply_message_id

    status: Feedback.status
    message: Feedback.message

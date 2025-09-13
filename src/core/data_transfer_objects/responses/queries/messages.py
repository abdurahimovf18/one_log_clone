from src.core.data_transfer_objects.base import BaseDTO
from src.core.domain_schema.models import Message


class GetCreatedMessageDTO(BaseDTO):
    id: Message.id
    text_id: Message.text_id | None = None
    owner_id: Message.owner_id
    interval: Message.interval
    duration: Message.duration


class CreateDTO(BaseDTO):
    id: Message.id
    text_id: Message.text_id | None = None
    owner_id: Message.owner_id
    interval: Message.interval
    duration: Message.duration
    started_at: Message.started_at | None = None
    status: Message.status

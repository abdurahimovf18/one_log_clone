from src.core.data_transfer_objects.base import BaseDTO
from src.core.domain_schema.models import Message


class GetCreatedMessageDTO(BaseDTO):
    owner_id: Message.owner_id


class GetLastByOwnerIdDTO(BaseDTO):
    owner_id: Message.owner_id


class CreateDTO(BaseDTO):
    owner_id: Message.owner_id
    

class UpdateTextIdByIdDTO(BaseDTO):
    id: Message.id
    text_id: Message.text_id


class UpdateIntervalByIdDTO(BaseDTO):
    id: Message.id
    interval: Message.interval


class UpdateDurationByIdDTO(BaseDTO):
    id: Message.id
    duration: Message.duration

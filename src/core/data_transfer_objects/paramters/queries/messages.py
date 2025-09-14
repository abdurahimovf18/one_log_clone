from src.core.data_transfer_objects.base import BaseDTO
from src.core.domain_schema.models import Message


class GetCreatedMessageDTO(BaseDTO):
    owner_id: Message.owner_id


class CreateDTO(BaseDTO):
    owner_id: Message.owner_id
    

from src.core.data_transfer_objects.base import BaseDTO
from src.core.domain_schema.models import Text


class CreateDTO(BaseDTO):
    id: Text.id
    content: Text.content
    


class GetByIdDTO(BaseDTO):
    content: Text.content

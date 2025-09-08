from src.core.data_transfer_objects.base import BaseDTO
from src.core.domain_schema.models import User


class CreateDTO(BaseDTO):
    id: User.id
    created_at: User.created_at
    

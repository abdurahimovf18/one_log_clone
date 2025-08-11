from src.core.data_transfer_objects.base import BaseDTO
from src.core.domain_schema.models import User


class CreateDTO(BaseDTO):
    id: User.id

    username: User.username
    password: User.password

    created_at: User.created_at
    updated_at: User.updated_at

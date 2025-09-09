from src.core.data_transfer_objects.base import BaseDTO
from src.core.domain_schema.models import UserAuth


class CreateDTO(BaseDTO):
    user_id: UserAuth.user_id
    username: UserAuth.username
    password: UserAuth.password
    updated_at: UserAuth.updated_at
    created_at: UserAuth.created_at


class GetPasswordByUsername(BaseDTO):
    password: UserAuth.password
    user_id: UserAuth.user_id
    
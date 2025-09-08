from src.core.data_transfer_objects.base import BaseDTO
from src.core.domain_schema.models import UserAuth


class CreateDTO(BaseDTO):
    username: UserAuth.username
    password: UserAuth.password
    

class GetPasswordByUsername(BaseDTO):
    username: UserAuth.username
    
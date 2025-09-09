from src.core.data_transfer_objects.base import BaseDTO
from src.core.domain_schema.models import UserAuth


class CreateDTO(BaseDTO):
    user_id: UserAuth.user_id
    username: UserAuth.username
    password: UserAuth.password
    

class GetPasswordByUsername(BaseDTO):
    username: UserAuth.username
    

class ExistsByUsernameDTO(BaseDTO):
    username: UserAuth.username

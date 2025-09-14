from src.core.data_transfer_objects.base import BaseDTO
from src.core.domain_schema.models import TgGroup


class GetPageByUserIdDTO(BaseDTO):
    username: TgGroup.username
    
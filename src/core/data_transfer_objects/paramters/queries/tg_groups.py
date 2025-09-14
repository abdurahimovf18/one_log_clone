from src.core.data_transfer_objects.base import BaseDTO
from src.core.domain_schema.models import TgGroup


class ExistsActiveByUserIdDTO(BaseDTO):
    owner_id: TgGroup.owner_id


class GetPageByUserIdDTO(BaseDTO):
    owner_id: TgGroup.owner_id
    page: int


from src.core.data_transfer_objects.base import BaseDTO
from src.core.domain_schema.models import TgAccount


class GetPageByUserIdDTO(BaseDTO):
    user_id: TgAccount.user_id
    page: int


class ExistsActiveByUserIdDTO(BaseDTO):
    user_id: TgAccount.user_id
    
from pydantic import Field

from src.core.data_transfer_objects.base import BaseDTO
from src.core.domain_schema.models import UserAuth


class ExistsDTO(BaseDTO):
    user_id: UserAuth.user_id | None = Field(default=None)
    chat_id: UserAuth.chat_id | None = Field(default=None)

from src.core.data_transfer_objects.base import BaseDTO
from src.core.domain_schema.models import UserLanguage


class GetByChatIdDTO(BaseDTO):
    language: UserLanguage.language

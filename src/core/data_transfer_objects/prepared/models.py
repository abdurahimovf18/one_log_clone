from pydantic import Field

from src.core.data_transfer_objects.base import BaseDTO
from src.core.domain_schema.models import User as UserDomainSchema
from src.core.domain_schema.models import UserAuth as UserAuthDomainSchema
from src.core.domain_schema.models import UserLanguage as UserLanguageDomainSchema

__all__ = [
    "UserAuthOptionalDTO",
    "UserLanguageOptionalDTO",
    "UserOptionalDTO",
]


class UserOptionalDTO(BaseDTO):
    id: UserDomainSchema.id | None = Field(default=None)

    username: UserDomainSchema.username | None = Field(default=None)
    password: UserDomainSchema.password | None = Field(default=None)

    created_at: UserDomainSchema.created_at | None = Field(default=None)
    updated_at: UserDomainSchema.updated_at | None = Field(default=None)


class UserAuthOptionalDTO(BaseDTO):
    user_id: UserAuthDomainSchema.user_id | None = Field(default=None)
    chat_id: UserAuthDomainSchema.chat_id | None = Field(default=None)


class UserLanguageOptionalDTO(BaseDTO):
    chat_id: UserLanguageDomainSchema.chat_id | None = Field(default=None)
    language: UserLanguageDomainSchema.language | None = Field(default=None)
    created_at: UserLanguageDomainSchema.created_at | None = Field(default=None)
    updated_at: UserLanguageDomainSchema.updated_at | None = Field(default=None)

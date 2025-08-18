from pydantic import Field

from src.core.data_transfer_objects.base import BaseDTO
from src.core.domain_schema.models import User


class CreateDTO(BaseDTO):
    username: User.username
    password: User.password


class ExistsDTO(BaseDTO):
    id: User.id | None = Field(default=None)
    username: User.username | None = Field(default=None)
    created_at: User.created_at | None = Field(default=None)
    updated_at: User.updated_at | None = Field(default=None)


class GetPasswordByUsername(BaseDTO):
    username: User.username
    
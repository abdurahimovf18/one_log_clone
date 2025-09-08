from typing import Annotated

from pydantic import Field

from src.core.domain_schema.shared_schema import UUID_ID, CreatedAt, UpdatedAt


class UserAuth:
    type user_id = UUID_ID

    type username = Annotated[str, Field()]
    type password = Annotated[str, Field()]
    
    type updated_at = UpdatedAt
    type created_at = CreatedAt

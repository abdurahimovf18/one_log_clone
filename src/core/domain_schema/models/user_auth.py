from typing import Annotated

from pydantic import Field

from src.core.domain_schema.shared_schema import CREATED_AT, UPDATED_AT, UUID_ID


class UserAuth:
    type user_id = UUID_ID

    type username = Annotated[str, Field()]
    type password = Annotated[str, Field()]
    
    type created_at = CREATED_AT
    type updated_at = UPDATED_AT

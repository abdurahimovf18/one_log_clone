from typing import Annotated

from pydantic import Field

from src.core.domain_schema.shared_schema import CREATED_AT, UPDATED_AT, UUID_ID


class TgGroup:
    type username = Annotated[str, Field()]
    type owner_id = UUID_ID
    type created_at = CREATED_AT
    type updated_at = UPDATED_AT

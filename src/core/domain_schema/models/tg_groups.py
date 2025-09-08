from typing import Annotated

from pydantic import Field

from src.core.domain_schema.shared_schema import UUID_ID, CreatedAt, UpdatedAt


class TgGroup:
    type username = Annotated[str, Field()]
    type owner_id = UUID_ID
    type created_at = CreatedAt
    type updated_at = UpdatedAt
    
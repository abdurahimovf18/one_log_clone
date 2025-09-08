from typing import Annotated

from pydantic import Field

from src.core.domain_schema.shared_schema import UUID_ID


class TgAccount:
    type session_id = UUID_ID
    type user_id = UUID_ID
    type phone = Annotated[str, Field()]

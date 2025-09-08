from typing import Annotated

from pydantic import Field

from src.core.domain_schema.shared_schema import UUID_ID


class Text:
    type id = UUID_ID
    type content = Annotated[str, Field()]

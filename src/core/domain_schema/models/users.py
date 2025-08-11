from typing import Annotated

from pydantic import Field

from src.core.domain_schema.shared_schema import ID, CreatedAt, UpdatedAt


class User:
    type id = ID

    type username = Annotated[str, Field()]
    type password = Annotated[str, Field()]

    type created_at = CreatedAt
    type updated_at = UpdatedAt

    type tg_auth = Annotated[list["UserTgAuth"], Field()]  # type: ignore  # noqa: F821

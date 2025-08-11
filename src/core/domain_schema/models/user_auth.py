from typing import Annotated

from pydantic import Field

from src.core.domain_schema.shared_schema import ID, ChatID


class UserAuth:
    type user_id = ID
    type chat_id = ChatID
    type user = Annotated[  # type: ignore
        "User",  # type: ignore  # noqa: F821
        Field()
    ]

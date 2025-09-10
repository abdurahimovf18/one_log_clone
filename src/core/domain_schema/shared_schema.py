import uuid
from datetime import datetime
from typing import Annotated

from pydantic import Field

type UUID_ID = Annotated[
    uuid.UUID,
    Field()
]

type CREATED_AT = Annotated[
    datetime,
    Field()
]

type UPDATED_AT = Annotated[
    datetime,
    Field()
]

type CHAT_ID = Annotated[
    int,
    Field()
]

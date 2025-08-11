import uuid
from datetime import datetime
from typing import Annotated

from pydantic import Field

type ID = Annotated[
    uuid.UUID,
    Field()
]

type CreatedAt = Annotated[
    datetime,
    Field()
]

type UpdatedAt = Annotated[
    datetime,
    Field()
]

type ChatID = Annotated[
    int,
    Field()
]

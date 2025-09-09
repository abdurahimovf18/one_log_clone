import uuid
from datetime import datetime
from functools import partial
from typing import Annotated

import sqlalchemy as sa
from sqlalchemy import types as sa_typ
from sqlalchemy.orm import mapped_column

from src.config.settings import TIMEZONE
from src.infrastructure.database import Base

__all__ = [
    "CREATED_AT",
    "ID",
    "UPDATED_AT",
    "Base",
]

type ID = Annotated[
    uuid.UUID,
    mapped_column(
        sa_typ.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4()
    )
]

type CREATED_AT = Annotated[
    datetime,
    mapped_column(
        sa_typ.DateTime(timezone=True),
        server_default=sa.text("TIMEZONE('UTC', NOW())"),
    )
]

type UPDATED_AT = Annotated[
    datetime,
    mapped_column(
        sa_typ.DateTime(timezone=True),
        server_default=sa.text("TIMEZONE('UTC', NOW())"),
        onupdate=partial(datetime.now, TIMEZONE)
    )
]


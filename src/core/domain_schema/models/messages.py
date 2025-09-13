from datetime import datetime, timedelta
from typing import Annotated

from pydantic import Field

from src.core.domain_schema.shared_schema import UUID_ID
from src.models.shared.enums import MessageStatus


class Message:
    type id = UUID_ID
    type text_id = UUID_ID
    type owner_id = UUID_ID
    type interval = Annotated[timedelta, Field()]
    type duration = Annotated[timedelta, Field()]
    type started_at = Annotated[datetime, Field()]
    type status = Annotated[MessageStatus, Field()]

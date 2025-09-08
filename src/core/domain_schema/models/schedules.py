from datetime import datetime, timedelta
from typing import Annotated

from pydantic import Field

from src.core.domain_schema.shared_schema import UUID_ID


class Schedule:
    type id = UUID_ID
    type text_id = UUID_ID
    type session_id = UUID_ID
    type start_at = Annotated[datetime, Field()]
    type interval = Annotated[timedelta, Field()]
    type repeat_count = Annotated[int, Field()]
    type max_repeat_count = Annotated[int, Field()]

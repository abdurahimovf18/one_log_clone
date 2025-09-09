import uuid
from datetime import datetime, timedelta

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from src.models.shared.base import ID, Base


class Schedule(Base):
    __tablename__ = "schedules"
    id: Mapped[ID]
    text_id: Mapped[uuid.UUID] = mapped_column(sa.ForeignKey("texts.id", ondelete="RESTRICT"))
    session_id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(as_uuid=True), 
        sa.ForeignKey("tg_accounts.session_id", ondelete="CASCADE")
    )
    start_at: Mapped[datetime]
    interval: Mapped[timedelta]
    repeat_count: Mapped[int]
    max_repeat_count: Mapped[int]

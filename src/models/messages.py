import uuid
from datetime import datetime, timedelta

import sqlalchemy as sa
from sqlalchemy import types as sa_typ
from sqlalchemy.orm import Mapped, mapped_column

from src.config.settings import DEFAULT_DURATION, DEFAULT_INTERVAL
from src.models.shared.base import ID, Base


class Messages(Base):
    __tablename__ = "messages"
    id: Mapped[ID]
    text_id: Mapped[uuid.UUID] = mapped_column(sa.ForeignKey("texts.id", ondelete="RESTRICT"))
    interval: Mapped[timedelta] = mapped_column(default=DEFAULT_INTERVAL.value)
    duration: Mapped[timedelta] = mapped_column(default=DEFAULT_DURATION.value)
    started_at: Mapped[datetime | None]
    owner_id: Mapped[uuid.UUID] = mapped_column(sa_typ.UUID(), sa.ForeignKey("users.id"))

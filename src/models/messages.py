import uuid
from datetime import datetime, timedelta

import sqlalchemy as sa
from sqlalchemy import types as sa_typ
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column

from src.config.settings import DEFAULT_DURATION, DEFAULT_INTERVAL, TIMEZONE
from src.models.shared.base import CREATED_AT, ID, Base
from src.models.shared.enums import MessageStatus


class Message(Base):
    __tablename__ = "messages"
    id: Mapped[ID]
    text_id: Mapped[uuid.UUID | None] = mapped_column(
        sa.ForeignKey("texts.id", ondelete="RESTRICT")
    )
    interval: Mapped[timedelta] = mapped_column(default=DEFAULT_INTERVAL.value)
    duration: Mapped[timedelta] = mapped_column(default=DEFAULT_DURATION.value)
    started_at: Mapped[datetime | None] = mapped_column(sa_typ.DateTime(timezone=True))
    owner_id: Mapped[uuid.UUID] = mapped_column(sa_typ.UUID(), sa.ForeignKey("users.id"))
    created_at: Mapped[CREATED_AT]

    @hybrid_property
    def status(self) -> MessageStatus:  # type: ignore
        now = datetime.now(TIMEZONE)
        if self.started_at is None:
            return MessageStatus.CREATED
        elif self.started_at + self.duration < now:
            return MessageStatus.STARTED
        elif self.started_at + self.duration >= now:
            return MessageStatus.FINISHED
        else:
            raise RuntimeError("Messages.status logic is wrong...")
        
    @status.expression
    def status(cls):
        return sa.case(
            (cls.started_at.is_(None), MessageStatus.CREATED),  # type: ignore
            (cls.started_at + cls.duration < sa.func.now(), MessageStatus.STARTED),  # type: ignore
            else_=MessageStatus.FINISHED
        )
    
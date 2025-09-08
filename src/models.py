import uuid
from datetime import datetime, timedelta
from functools import partial
from typing import Annotated

import sqlalchemy as sa
from sqlalchemy import types as sa_typ
from sqlalchemy.orm import Mapped, mapped_column

from src.config.settings import DEFAULT_DURATION, DEFAULT_INTERVAL, DEFAULT_LANGUAGE, TIMEZONE
from src.core.domain_schema.settings import UserLanguages
from src.infrastructure.database import Base

id_ = Annotated[
    uuid.UUID,
    mapped_column(
        sa_typ.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4()
    )
]

created_at = Annotated[
    datetime,
    mapped_column(
        sa_typ.DateTime(timezone=True),
        server_default=sa.text("TIMEZONE('UTC', NOW())"),
    )
]

updated_at = Annotated[
    datetime,
    mapped_column(
        sa_typ.DateTime(timezone=True),
        server_default=sa.text("TIMEZONE('UTC', NOW())"),
        onupdate=partial(datetime.now, TIMEZONE)
    )
]


class User(Base):
    __tablename__ = "users"
    id: Mapped[id_]
    created_at: Mapped[created_at]


class UserAuth(Base):
    __tablename__ = "user_auth"
    user_id: Mapped[uuid.UUID] = mapped_column(
        sa_typ.UUID(as_uuid=True), sa.ForeignKey("users.id"), primary_key=True
    )
    username: Mapped[str] = mapped_column(sa_typ.String(255), unique=True, index=True)
    password: Mapped[str] = mapped_column(sa_typ.String(255))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


class TgUser(Base):
    __tablename__ = "tg_users"
    chat_id: Mapped[int] = mapped_column(sa_typ.BigInteger, primary_key=True)
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        sa.ForeignKey("users.id", ondelete="SET NULL")
    )
    language: Mapped[UserLanguages] = mapped_column(
        sa_typ.Enum(UserLanguages), default=DEFAULT_LANGUAGE
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


class TgGroup(Base):
    __tablename__ = "tg_groups"
    username: Mapped[str] = mapped_column(sa_typ.String(255), primary_key=True)
    owner_id: Mapped[uuid.UUID] = mapped_column(
        sa_typ.UUID(), sa.ForeignKey("users.id"), primary_key=True
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


class TgAccount(Base):
    __tablename__ = "tg_accounts"
    session_id: Mapped[id_]
    user_id: Mapped[uuid.UUID] = mapped_column(sa_typ.UUID(as_uuid=True), sa.ForeignKey("users.id"))
    phone: Mapped[str] = mapped_column(sa_typ.String(25))
    # TODO: status for deleting and unexpected behaviours

    __table_args__ = (
        sa.UniqueConstraint("user_id", "phone", name="user_id_phone_unique_constraint"),
    )


class Messages(Base):
    __tablename__ = "messages"
    id: Mapped[id_]
    text_id: Mapped[uuid.UUID] = mapped_column(sa.ForeignKey("texts.id", ondelete="RESTRICT"))
    interval: Mapped[timedelta] = mapped_column(default=DEFAULT_INTERVAL.value)
    duration: Mapped[timedelta] = mapped_column(default=DEFAULT_DURATION.value)
    started_at: Mapped[datetime | None]
    owner_id: Mapped[uuid.UUID] = mapped_column(sa_typ.UUID(), sa.ForeignKey("users.id"))


class Texts(Base):
    __tablename__ = "texts"
    id: Mapped[id_]
    content: Mapped[str]


class Schedule(Base):
    __tablename__ = "schedules"
    id: Mapped[id_]
    text_id: Mapped[uuid.UUID] = mapped_column(sa.ForeignKey("texts.id", ondelete="RESTRICT"))
    session_id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(as_uuid=True), 
        sa.ForeignKey("tg_accounts.session_id", ondelete="CASCADE")
    )
    start_at: Mapped[datetime]
    interval: Mapped[timedelta]
    repeat_count: Mapped[int]
    max_repeat_count: Mapped[int]

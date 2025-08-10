import uuid
from datetime import datetime
from functools import partial
from typing import Annotated

import sqlalchemy as sa
from sqlalchemy import types as sa_typ
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.settings import TIMEZONE
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

    username: Mapped[str]
    password: Mapped[str]

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    tg_auth: Mapped[list["UserTgAuth"]] = relationship(
        "UserTgAuth", back_populates="user", uselist=True
    )


class UserTgAuth(Base):
    __tablename__ = "user_tg_auth"

    user_id: Mapped[uuid.UUID] = mapped_column(
        sa_typ.UUID(as_uuid=True), 
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    chat_id: Mapped[int] = mapped_column(sa_typ.Integer, primary_key=True)

    user: Mapped["User"] = relationship("User", back_populates="tg_auth")


class UserLanguage(Base):
    __tablename__ = "user_languages"

    chat_id: Mapped[int] = mapped_column(sa_typ.Integer, primary_key=True)  # for private users
    language: Mapped[str]

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

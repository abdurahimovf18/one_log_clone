import uuid
from datetime import datetime
from functools import partial
from typing import Annotated

import sqlalchemy as sa
from sqlalchemy import types as sa_typ
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.settings import DEFAULT_LANGUAGE, TIMEZONE
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

    username: Mapped[str]
    password: Mapped[str]

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    tg_auth: Mapped[list["UserAuth"]] = relationship(
        "UserAuth", back_populates="user", uselist=True
    )


class UserAuth(Base):
    __tablename__ = "user_auth"

    user_id: Mapped[uuid.UUID] = mapped_column(
        sa_typ.UUID(as_uuid=True), 
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    chat_id: Mapped[int] = mapped_column(sa_typ.BigInteger, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="tg_auth")

    __table_args__ = (
        sa.Index("user_auth_chat_id_inx", "chat_id"),
    )


class UserLanguage(Base):
    __tablename__ = "user_languages"

    chat_id: Mapped[int] = mapped_column(sa_typ.BigInteger, primary_key=True)  # for private users
    language: Mapped[UserLanguages] = mapped_column(
        sa_typ.Enum(UserLanguages), default=DEFAULT_LANGUAGE
    )

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

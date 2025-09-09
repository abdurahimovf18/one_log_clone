import uuid

import sqlalchemy as sa
from sqlalchemy import types as sa_typ
from sqlalchemy.orm import Mapped, mapped_column

from src.config.settings import DEFAULT_LANGUAGE
from src.models.shared.base import CREATED_AT, UPDATED_AT, Base
from src.models.shared.enums import Languages


class TgUser(Base):
    __tablename__ = "tg_users"
    chat_id: Mapped[int] = mapped_column(sa_typ.BigInteger, primary_key=True)
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        sa.ForeignKey("users.id", ondelete="SET NULL")
    )
    language: Mapped[Languages] = mapped_column(
        default=DEFAULT_LANGUAGE
    )
    created_at: Mapped[CREATED_AT]
    updated_at: Mapped[UPDATED_AT]
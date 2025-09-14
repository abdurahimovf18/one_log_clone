import uuid

import sqlalchemy as sa
from sqlalchemy import types as sa_typ
from sqlalchemy.orm import Mapped, mapped_column

from src.models.shared.base import CREATED_AT, UPDATED_AT, Base


class TgGroup(Base):
    __tablename__ = "tg_groups"
    username: Mapped[str] = mapped_column(sa_typ.String(255), primary_key=True)
    owner_id: Mapped[uuid.UUID] = mapped_column(
        sa_typ.UUID(), sa.ForeignKey("users.id"), primary_key=True
    )
    created_at: Mapped[CREATED_AT]
    updated_at: Mapped[UPDATED_AT]

    is_active: Mapped[bool] = mapped_column(default=True)
    
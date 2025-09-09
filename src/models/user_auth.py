import uuid

import sqlalchemy as sa
from sqlalchemy import types as sa_typ
from sqlalchemy.orm import Mapped, mapped_column

from src.models.shared.base import CREATED_AT, UPDATED_AT, Base


class UserAuth(Base):
    __tablename__ = "user_auth"
    user_id: Mapped[uuid.UUID] = mapped_column(
        sa_typ.UUID(as_uuid=True), sa.ForeignKey("users.id"), primary_key=True
    )
    username: Mapped[str] = mapped_column(sa_typ.String(255), unique=True, index=True)
    password: Mapped[str] = mapped_column(sa_typ.String(255))
    created_at: Mapped[CREATED_AT]
    updated_at: Mapped[UPDATED_AT]

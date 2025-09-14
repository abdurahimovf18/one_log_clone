import uuid

import sqlalchemy as sa
from sqlalchemy import types as sa_typ
from sqlalchemy.orm import Mapped, mapped_column

from src.models.shared.base import ID, Base


class TgAccount(Base):
    __tablename__ = "tg_accounts"
    session_id: Mapped[ID]
    user_id: Mapped[uuid.UUID] = mapped_column(sa_typ.UUID(as_uuid=True), sa.ForeignKey("users.id"))
    phone: Mapped[str] = mapped_column(sa_typ.String(25))
    # TODO: status for deleting and unexpected behaviours

    is_active: Mapped[bool] = mapped_column(default=True)

    __table_args__ = (
        sa.UniqueConstraint("user_id", "phone", name="user_id_phone_unique_constraint"),
    )
from sqlalchemy import types as sa_typ
from sqlalchemy.orm import Mapped, mapped_column

from src.models.shared.base import CREATED_AT, ID, UPDATED_AT, Base
from src.models.shared.enums import FeedbackStatus


class Feedback(Base):
    __tablename__ = "feedbacks"

    id: Mapped[ID]
    chat_id: Mapped[int] = mapped_column(sa_typ.BigInteger, index=True)
    user_id: Mapped[int] = mapped_column(sa_typ.BigInteger, index=True)
    reply_message_id: Mapped[int]

    status: Mapped[FeedbackStatus] = mapped_column(default=FeedbackStatus.NEW)
    message: Mapped[str] = mapped_column(sa_typ.String(length=2048))
    
    created_at: Mapped[CREATED_AT]
    updated_at: Mapped[UPDATED_AT]

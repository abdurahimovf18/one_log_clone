from sqlalchemy.orm import Mapped

from src.models.shared.base import CREATED_AT, ID, Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[ID]
    created_at: Mapped[CREATED_AT]

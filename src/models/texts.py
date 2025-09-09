from sqlalchemy.orm import Mapped

from src.models.shared.base import ID, Base


class Texts(Base):
    __tablename__ = "texts"
    id: Mapped[ID]
    content: Mapped[str]

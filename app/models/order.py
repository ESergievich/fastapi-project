from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models import Base


class Order(Base):
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

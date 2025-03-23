from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base

if TYPE_CHECKING:
    from models import User, Product, OrderItem


class Order(Base):
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    user: Mapped["User"] = relationship(back_populates="orders")
    products: Mapped[list["Product"]] = relationship(
        back_populates="orders", secondary="order_items", viewonly=True
    )
    order_items: Mapped[list["OrderItem"]] = relationship(back_populates="order")

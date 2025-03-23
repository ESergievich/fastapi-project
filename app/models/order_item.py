from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base

if TYPE_CHECKING:
    from models import Order, Product


class OrderItem(Base):
    id = None
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
        index=True,
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="RESTRICT"),
        primary_key=True,
        nullable=False,
        index=True,
    )
    quantity: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint("quantity > 0", name="quantity_positive"),
        nullable=False,
        default=1,
    )

    order: Mapped["Order"] = relationship(back_populates="order_items")
    product: Mapped["Product"] = relationship(back_populates="order_items")

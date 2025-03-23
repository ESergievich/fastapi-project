from typing import Optional, TYPE_CHECKING

from slugify import slugify
from sqlalchemy import String, Float, Text, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from models import Base

if TYPE_CHECKING:
    from models import Order, OrderItem


class Product(Base):
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    slug: Mapped[Optional[str]] = mapped_column(String(255), unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(
        Float, CheckConstraint("price > 0", name="price_positive"), nullable=False
    )

    orders: Mapped[list["Order"]] = relationship(
        back_populates="products", secondary="order_items", viewonly=True
    )
    order_items: Mapped[list["OrderItem"]] = relationship(back_populates="product")

    @validates("slug")
    def generate_slug(self, _, value):
        return value or slugify(self.name)

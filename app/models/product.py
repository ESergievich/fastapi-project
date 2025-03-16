from typing import Optional

from slugify import slugify
from sqlalchemy import String, Float, Text, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, validates

from models import Base


class Product(Base):
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    slug: Mapped[Optional[str]] = mapped_column(String(255), unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(
        Float, CheckConstraint("price > 0", name="price_positive"), nullable=False
    )

    @validates("slug")
    def generate_slug(self, _, value):
        return value or slugify(self.name)

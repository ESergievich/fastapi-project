from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from utils import RoleEnum

if TYPE_CHECKING:
    from .order import Order


class User(Base, SQLAlchemyBaseUserTable[int]):
    username: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[RoleEnum] = mapped_column(
        Enum(RoleEnum), nullable=False, server_default=RoleEnum.CUSTOMER.name
    )

    orders: Mapped[list["Order"]] = relationship(back_populates="user")

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from utils import RoleEnum


class User(Base, SQLAlchemyBaseUserTable[int]):
    username: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[RoleEnum] = mapped_column(
        Enum(RoleEnum), nullable=False, server_default=RoleEnum.CUSTOMER.name
    )

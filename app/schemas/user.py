from typing import Optional

from fastapi_users.schemas import BaseUserCreate, BaseUserUpdate, BaseUser

from utils import RoleEnum


class UserRead(BaseUser[int]):
    username: Optional[str] = None
    role: RoleEnum = RoleEnum.CUSTOMER


class UserCreate(BaseUserCreate):
    username: Optional[str] = None
    role: RoleEnum = RoleEnum.CUSTOMER


class UserUpdate(BaseUserUpdate):
    username: Optional[str] = None
    role: Optional[RoleEnum] = None

from typing import Optional

from fastapi_users.schemas import BaseUserCreate, BaseUserUpdate, BaseUser

from utils import RoleEnum


class UserRead(BaseUser[int]):
    username: str
    role: RoleEnum = RoleEnum.CUSTOMER


class UserCreate(BaseUserCreate):
    username: str


class UserAdminCreate(UserCreate):
    role: RoleEnum = RoleEnum.ADMIN


class UserUpdate(BaseUserUpdate):
    username: Optional[str] = None

from fastapi_users.schemas import BaseUserCreate, BaseUserUpdate, BaseUser


class UserRead(BaseUser[int]):
    pass


class UserCreate(BaseUserCreate):
    pass


class UserUpdate(BaseUserUpdate):
    pass

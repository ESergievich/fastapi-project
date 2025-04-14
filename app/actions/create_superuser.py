import asyncio
import contextlib
from typing import TYPE_CHECKING

from fastapi_users.exceptions import UserAlreadyExists
from pydantic import EmailStr

from authentication import get_user_db, get_user_manager, UserManager
from core import db_helper
from schemas import UserAdminCreate
from utils import RoleEnum

if TYPE_CHECKING:
    from models import User


get_users_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


default_email = "admin@admin.com"
default_password = "admin"
default_is_active = True
default_is_superuser = True
default_is_verified = True
default_username = "admin"
default_role = RoleEnum.ADMIN


async def create_user(
    user_manager: UserManager,
    user_create: UserAdminCreate,
) -> "User":
    user = await user_manager.create(
        user_create=user_create,
        safe=False,
    )
    return user


async def create_superuser(
    email: EmailStr = default_email,
    password: str = default_password,
    is_active: bool = default_is_active,
    is_superuser: bool = default_is_superuser,
    is_verified: bool = default_is_verified,
    username: str = default_username,
    role: RoleEnum = default_role,
):
    user_create = UserAdminCreate(
        email=email,
        password=password,
        is_active=is_active,
        is_superuser=is_superuser,
        is_verified=is_verified,
        username=username,
        role=role,
    )
    try:
        async with db_helper.session_factory() as session:
            async with get_users_db_context(session) as users_db:
                async with get_user_manager_context(users_db) as user_manager:
                    return await create_user(
                        user_manager=user_manager,
                        user_create=user_create,
                    )
    except UserAlreadyExists:
        pass


if __name__ == "__main__":
    asyncio.run(create_superuser())

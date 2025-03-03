from typing import TYPE_CHECKING, Annotated

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyAccessTokenDatabase

from core import db_helper
from models import User, AccessToken
from .user_manager import UserManager

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase as SQLAlchemyUserDatabaseType

async def get_user_db(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
):
    yield SQLAlchemyUserDatabase(session, User)


async def get_access_tokens_db(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
):
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken)


async def get_user_manager(
    users_db: Annotated["SQLAlchemyUserDatabaseType", Depends(get_user_db)],
):
    yield UserManager(users_db)

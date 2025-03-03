from typing import Annotated, TYPE_CHECKING

from fastapi import Depends
from fastapi_users.authentication.strategy import DatabaseStrategy

from core import settings
from .dependencies import get_access_tokens_db

if TYPE_CHECKING:
    from models import AccessToken
    from fastapi_users.authentication.strategy.db import AccessTokenDatabase


def get_database_strategy(
        access_tokens_db: Annotated["AccessTokenDatabase[AccessToken]", Depends(get_access_tokens_db)]
) -> DatabaseStrategy:
    return DatabaseStrategy(
        database=access_tokens_db,
        lifetime_seconds=settings.access_token.lifetime_seconds,
    )

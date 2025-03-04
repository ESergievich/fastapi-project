from fastapi import APIRouter

from authentication import fastapi_users
from core import settings
from schemas import UserRead, UserUpdate

router = APIRouter(
    prefix=settings.api.v1.users,
    tags=["Users"],
)

# /me
# /{id}
router.include_router(
    router=fastapi_users.get_users_router(
        UserRead,
        UserUpdate,
    ),
)

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from authentication import fastapi_users
from core import settings
from schemas import UserRead, UserUpdate

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix=settings.api.v1.users,
    tags=["Users"],
    dependencies=[Depends(http_bearer)],
)

# /me
# /{id}
router.include_router(
    router=fastapi_users.get_users_router(
        UserRead,
        UserUpdate,
    ),
)

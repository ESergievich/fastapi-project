from fastapi import APIRouter

from core import settings
from .auth import router as auth_router
from .users import router as users_router
from .base_router import create_base_router
from .products import router as products_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)

router.include_router(auth_router)
router.include_router(users_router)

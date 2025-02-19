from fastapi import APIRouter

from core import settings

router = APIRouter(
    prefix=settings.api.v1.prefix,
)

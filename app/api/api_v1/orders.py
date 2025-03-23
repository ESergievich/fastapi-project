from fastapi import APIRouter

from api.api_v1 import create_base_router
from core import settings
from schemas import OrderUpdate, OrderResponse, OrderCreate, OrderFilterIn
from service import order_service

router = APIRouter(
    prefix=settings.api.v1.orders,
    tags=["Orders"],
)

router.include_router(
    router=create_base_router(
        service=order_service,
        create_schema=OrderCreate,
        update_schema=OrderUpdate,
        response_schema=OrderResponse,
        filter_in_schema=OrderFilterIn,
    )
)

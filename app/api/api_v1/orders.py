from fastapi import APIRouter

from api.api_v1 import create_base_router
from core import settings
from dependencies import role_required
from schemas import OrderUpdate, OrderResponse, OrderCreate, OrderFilterIn
from service import order_service
from utils import RoleEnum

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
        permission_map={
            "create": role_required(
                RoleEnum.ADMIN, RoleEnum.MANAGER, RoleEnum.CUSTOMER
            ),
            "get": role_required(RoleEnum.ADMIN, RoleEnum.MANAGER, RoleEnum.CUSTOMER),
            "get_all": role_required(
                RoleEnum.ADMIN, RoleEnum.MANAGER, RoleEnum.CUSTOMER
            ),
            "update": role_required(
                RoleEnum.ADMIN, RoleEnum.MANAGER, RoleEnum.CUSTOMER
            ),
            "delete": role_required(
                RoleEnum.ADMIN, RoleEnum.MANAGER, RoleEnum.CUSTOMER
            ),
        },
    )
)

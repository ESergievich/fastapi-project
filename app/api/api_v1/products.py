from fastapi import APIRouter

from api.api_v1 import create_base_router
from core import settings
from schemas import ProductUpdate, ProductResponse, ProductCreate, ProductFilterIn
from service import product_service

router = APIRouter(
    prefix=settings.api.v1.products,
    tags=["Products"],
)

router.include_router(
    router=create_base_router(
        service=product_service,
        create_schema=ProductCreate,
        update_schema=ProductUpdate,
        response_schema=ProductResponse,
        filter_in_schema=ProductFilterIn,
    )
)

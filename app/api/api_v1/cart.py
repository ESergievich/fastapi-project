from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends
from starlette import status

from core import settings, db_helper
from redis_cache import get_cart_service
from schemas import CartResponse, CartItem, OrderResponse

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from redis_cache import CartRedis

router = APIRouter(
    prefix=settings.api.v1.cart,
    tags=["Cart"],
)


@router.post(
    "/{user_id}/add",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
)
async def add_to_cart(
    item: CartItem, cart: "CartRedis" = Depends(get_cart_service)
) -> CartResponse:
    """Adds a product to the cart or increases its quantity."""

    return CartResponse(items=await cart.add_to_cart(item))


@router.get(
    "/{user_id}",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
)
async def get_cart(cart=Depends(get_cart_service)) -> CartResponse:
    """Retrieves the contents of the cart."""

    return CartResponse(items=await cart.get_cart())


@router.patch(
    "/{user_id}/remove",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
)
async def remove_from_cart(
    item: CartItem, cart=Depends(get_cart_service)
) -> CartResponse:
    """Decreases the quantity of a product or removes it if the quantity is ≤ 0."""

    return CartResponse(items=await cart.remove_from_cart(item))


@router.delete("/{user_id}/clear", status_code=status.HTTP_200_OK)
async def remove_from_cart(cart=Depends(get_cart_service)) -> dict:
    """Clears the user's cart."""

    await cart.clear_cart()
    return {"message": "User's cart is cleared"}


@router.post(
    "/{user_id}/checkout",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
)
async def checkout(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
    cart=Depends(get_cart_service),
) -> OrderResponse:
    """Creates an order with the products in user's cart."""

    return await cart.checkout(session)

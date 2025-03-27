from typing import TYPE_CHECKING

from fastapi import Depends


from redis_cache import get_redis
from schemas import OrderCreate, OrderItemCreate
from service import order_service

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from redis.asyncio import Redis
    from schemas import CartItem, OrderResponse


class CartRedis:
    """Service for working with the cart in Redis."""

    def __init__(self, redis: "Redis", user_id: int) -> None:
        self.redis = redis
        self.user_id = user_id
        self.cart_key: str = f"cart:{user_id}"
        self.expire_time: int = 3600  # 1 час

    async def add_to_cart(self, item: "CartItem") -> dict[str, str]:
        """Adds a product to the cart or increases its quantity."""

        async with self.redis.pipeline() as pipe:
            exists = await self.redis.hexists(self.cart_key, str(item.product_id))

            if exists:
                await pipe.hincrby(self.cart_key, str(item.product_id), item.quantity)
            else:
                await pipe.hset(self.cart_key, str(item.product_id), str(item.quantity))
                await pipe.expire(self.cart_key, self.expire_time)

            await pipe.execute()

        return await self.get_cart()

    async def get_cart(self) -> dict[str, str]:
        """Returns the contents of the cart."""

        return await self.redis.hgetall(self.cart_key)

    async def remove_from_cart(self, item: "CartItem") -> dict[str, str]:
        """Decreases the quantity of a product or removes it if the quantity is ≤ 0."""

        async with self.redis.pipeline() as pipe:
            exists = await self.redis.hexists(self.cart_key, str(item.product_id))

            if exists:
                new_quantity = await self.redis.hincrby(
                    self.cart_key, str(item.product_id), -item.quantity
                )

                if new_quantity <= 0:
                    await self.redis.hdel(self.cart_key, str(item.product_id))

            await pipe.execute()

        return await self.get_cart()

    async def clear_cart(self) -> None:
        """Clears the user's cart."""

        await self.redis.delete(self.cart_key)

    async def checkout(self, session: "AsyncSession") -> "OrderResponse":
        """Creates an order with the products in user's cart."""

        cart_items = await self.get_cart()
        order_in = OrderCreate(
            user_id=self.user_id,
            order_items=[
                OrderItemCreate(product_id=int(product_id), quantity=int(quantity))
                for product_id, quantity in cart_items.items()
            ],
        )
        order = await order_service.create(object_in=order_in, session=session)
        await self.clear_cart()
        return order


async def get_cart_service(user_id: int, redis=Depends(get_redis)) -> CartRedis:
    """Returns a service object for working with the user's cart in Redis."""

    return CartRedis(redis, user_id)

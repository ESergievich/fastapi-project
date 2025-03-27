from redis.asyncio import Redis
from app.core.config import settings


redis = Redis(
    host=settings.redis.host,
    port=settings.redis.port,
    decode_responses=settings.redis.decode_responses,
)


async def get_redis() -> Redis:
    """Get a Redis connection (dependency)."""

    return redis

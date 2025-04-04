import asyncio
from typing import TYPE_CHECKING, Optional

import aio_pika

if TYPE_CHECKING:
    from aio_pika.abc import AbstractRobustConnection, AbstractRobustChannel

from core import settings


class RabbitBase:
    def __init__(self):
        self._connection: Optional["AbstractRobustConnection"] = None
        self._channel: Optional["AbstractRobustChannel"] = None
        self.stop_event = asyncio.Event()

    @staticmethod
    async def get_connection() -> "AbstractRobustConnection":
        """Returns a connection to RabbitMQ."""
        return await aio_pika.connect_robust(settings.rabbitmq.url)

    @property
    def channel(self) -> "AbstractRobustChannel":
        """Returns a channel for RabbitMQ."""
        if self._channel is None:
            raise Exception("Please use context manager for Rabbit helper.")
        return self._channel

    async def __aenter__(self):
        self._connection = await self.get_connection()
        self._channel = await self._connection.channel()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.stop_event.set()
        if self._channel and not self._channel.is_closed:
            await self._channel.close()
        if self._connection and not self._connection.is_closed:
            await self._connection.close()

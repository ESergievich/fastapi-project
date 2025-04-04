import json
from typing import TYPE_CHECKING, Optional

from aio_pika import ExchangeType, Message
from aio_pika.abc import AbstractIncomingMessage, DeliveryMode

if TYPE_CHECKING:
    from aio_pika.abc import AbstractRobustExchange

from core import settings
from rabbit import RabbitBase
from utils import send_email


class RabbitEmailProcessor(RabbitBase):
    def __init__(self):
        super().__init__()
        self.exchange: Optional["AbstractRobustExchange"] = None

    async def create_exchange(self):
        """Create an exchange"""
        if not self.exchange:
            self.exchange = await self.channel.declare_exchange(
                name=settings.rmq_email_processor.exchange_name,
                type=ExchangeType.TOPIC,
            )

    async def publish_message(self, routing_key: str, message: dict):
        """Send a message to the queue"""
        await self.create_exchange()
        await self.exchange.publish(
            Message(
                body=json.dumps(message).encode(), delivery_mode=DeliveryMode.PERSISTENT
            ),
            routing_key=routing_key,
        )

    async def consume_message(
        self,
        prefetch_count: int = settings.rmq_email_processor.prefetch_count,
    ):
        """Get a message from the queue"""
        await self.channel.set_qos(prefetch_count=prefetch_count)
        await self.create_exchange()

        async def setup_queue(name, routing_key):
            queue = await self.channel.declare_queue(name=name, durable=True)
            await queue.bind(self.exchange, routing_key=routing_key)
            await queue.consume(self.process_message)

        await setup_queue(
            settings.rmq_email_processor.register_queue,
            settings.rmq_email_processor.routing_key_register,
        )
        await setup_queue(
            settings.rmq_email_processor.verification_queue,
            settings.rmq_email_processor.routing_key_verification,
        )
        await setup_queue(
            settings.rmq_email_processor.reset_password_queue,
            settings.rmq_email_processor.routing_key_reset_password,
        )

        await self.stop_event.wait()

    @staticmethod
    async def process_message(message: "AbstractIncomingMessage") -> None:
        """Processing messages from the queue"""
        async with message.process():
            data = json.loads(message.body)
            send_email(data["email"], data["subject"], data["body"])

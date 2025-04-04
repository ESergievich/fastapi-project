import logging
from typing import TYPE_CHECKING, Optional

from fastapi_users import BaseUserManager, IntegerIDMixin

from core import settings
from models import User
from rabbit import RabbitEmailProcessor

if TYPE_CHECKING:
    from fastapi import Request

log = logging.getLogger(__name__)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.access_token.reset_password_token_secret
    verification_token_secret = settings.access_token.verification_token_secret

    async def on_after_register(
        self,
        user: User,
        request: Optional["Request"] = None,
    ):
        log.warning("User %r has registered.", user.id)
        verification_link = (
            f"{settings.api.prefix_with_version}/auth/request-verify-token"
        )
        message = {
            "email": user.email,
            "subject": "Welcome to Our Service!",
            "body": f"Thank you for registering! Please verify your email by clicking the link below.\n\n{verification_link}",
        }

        async with RabbitEmailProcessor() as rabbit_processor:
            await rabbit_processor.publish_message(
                routing_key=settings.rmq_email_processor.routing_key_register,
                message=message,
            )

    async def on_after_request_verify(
        self,
        user: User,
        token: str,
        request: Optional["Request"] = None,
    ):
        log.warning(
            "Verification requested for user %r. Verification token: %r",
            user.id,
            token,
        )
        verification_link = (
            f"{settings.api.prefix_with_version}/auth/verify?token={token}"
        )
        message = {
            "email": user.email,
            "subject": "Email verification",
            "body": f"Follow the link to confirm: {verification_link}",
        }

        async with RabbitEmailProcessor() as rabbit_processor:
            await rabbit_processor.publish_message(
                routing_key=settings.rmq_email_processor.routing_key_verification,
                message=message,
            )

    async def on_after_forgot_password(
        self,
        user: User,
        token: str,
        request: Optional["Request"] = None,
    ):
        log.warning(
            "User %r has forgot their password. Reset token: %r",
            user.id,
            token,
        )
        reset_password_link = (
            f"{settings.api.prefix_with_version}/auth/reset-password?token={token}"
        )
        message = {
            "email": user.email,
            "subject": "Password reset",
            "body": f"Follow the link for password reset: {reset_password_link}",
        }

        async with RabbitEmailProcessor() as rabbit_processor:
            await rabbit_processor.publish_message(
                routing_key=settings.rmq_email_processor.routing_key_reset_password,
                message=message,
            )

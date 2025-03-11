import logging

from api_clients import AsyncHTTPClient

logger = logging.getLogger("api")


class AuthClient:
    """Клиент для работы с API аутентификации"""

    POST_REGISTER = "/auth/register"
    POST_LOGIN = "/auth/login"
    POST_REQUEST_VERIFY_TOKEN = "/auth/request-verify-token"
    POST_VERIFY_EMAIL = "/auth/verify"
    POST_FORGOT_PASSWORD = "/auth/forgot-password"
    POST_RESET_PASSWORD = "/auth/reset-password"

    def __init__(self, http_client: AsyncHTTPClient):
        self.client = http_client

    async def register_user(self, email: str, password: str):
        """Регистрация пользователя"""
        response = await self.client.custom_request(
            method="POST",
            endpoint=self.POST_REGISTER,
            json={"email": email, "password": password},
        )
        logger.info(f"Регистрация: {response.status_code} {response.text}")
        return response

    async def login(self, email: str, password: str):
        """Авторизация"""
        response = await self.client.custom_request(
            method="POST",
            endpoint=self.POST_LOGIN,
            data={"username": email, "password": password},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        logger.info(f"Логин: {response.status_code} {response.text}")
        return response

    async def request_verify_token(self, email: str):
        """Запросить токен подтверждения email"""
        response = await self.client.custom_request(
            method="POST",
            endpoint=self.POST_REQUEST_VERIFY_TOKEN,
            json={"email": email},
        )
        return response

    async def verify_email(self, token: str):
        """Подтвердить email"""
        response = await self.client.custom_request(
            method="POST",
            endpoint=self.POST_VERIFY_EMAIL,
            json={"token": token},
        )
        return response

    async def forgot_password(self, email: str):
        """Запрос на восстановление пароля"""
        response = await self.client.custom_request(
            method="POST",
            endpoint=self.POST_FORGOT_PASSWORD,
            json={"email": email},
        )
        return response

    async def reset_password(self, token: str, new_password: str):
        """Сброс пароля"""
        response = await self.client.custom_request(
            method="POST",
            endpoint=self.POST_RESET_PASSWORD,
            json={"token": token, "password": new_password},
        )
        return response

import pytest

from tests.api_clients import AuthClient
from tests.data import FakeUser
from tests.utils import create_verify_token


@pytest.mark.asyncio
class TestAuth:
    # Тест: Регистрация пользователя
    async def test_register_user(self, auth_client: AuthClient, user: FakeUser):
        response = await auth_client.register_user(
            email=user.email, password=user.password
        )
        assert response.status_code == 201
        assert "id" in response.json()
        user.id = response.json()["id"]

    # Тест: Запрос верификационного токена
    async def test_request_verify_token(self, auth_client: AuthClient, user: FakeUser):
        response = await auth_client.request_verify_token(email=user.email)
        assert response.status_code == 202
        user.verify_token = create_verify_token(user)

    # Тест: Подтверждение email
    async def test_verify_email(self, auth_client: AuthClient, user: FakeUser):
        response = await auth_client.verify_email(token=user.verify_token)
        assert response.status_code == 200
        user.is_verified = True

    # Тест: Логин
    async def test_login(self, auth_client: AuthClient, user: FakeUser):
        response = await auth_client.login(email=user.email, password=user.password)
        assert response.status_code == 200
        assert "access_token" in response.json()
        user.access_token = response.json()["access_token"]

    # Тест: Запрос на восстановление пароля
    async def test_forgot_password(self, auth_client: AuthClient, user: FakeUser):
        response = await auth_client.forgot_password(email=user.email)
        assert response.status_code == 202

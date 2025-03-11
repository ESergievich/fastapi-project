import asyncio

import pytest
import pytest_asyncio

from api_clients import AsyncHTTPClient, AuthClient
from data import FakeUser

BASE_URL = "http://localhost:8000/api/v1"


@pytest_asyncio.fixture(scope="session")
async def http_client():
    client = AsyncHTTPClient(BASE_URL)
    yield client
    await client.close()


@pytest_asyncio.fixture
async def auth_client(http_client):
    return AuthClient(http_client)


@pytest_asyncio.fixture(scope="session")
async def user():
    return FakeUser.random()


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

from typing import TYPE_CHECKING

from httpx import AsyncClient

if TYPE_CHECKING:
    from httpx import Response, URL


class AsyncHTTPClient:
    """Асинхронный HTTP-клиент для API-запросов"""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = AsyncClient(base_url=base_url)

    async def custom_request(
        self, method: str, endpoint: "URL | str", **kwargs
    ) -> "Response":
        """Выполняет HTTP-запрос"""
        url = f"{self.base_url}{endpoint}"
        response = await self.client.request(method, url, **kwargs)
        return response

    async def close(self):
        """Закрывает соединение"""
        await self.client.aclose()

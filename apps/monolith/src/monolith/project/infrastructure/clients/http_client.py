import httpx

from monolith.project.application.interfaces.client import IApiClient
from monolith.project.application.exceptions import api_client_exception as exceptions


class HttpxApiClient(IApiClient):
    """Реализация универсального асинхронного клиента на httpx"""

    def __init__(self, url: str, timeout: int = 10):
        self.timeout = timeout
        self.base_url = url
        # Создание клиент
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=timeout
        )

    async def get(self, endpoint: str, headers: dict = None, params: dict = None) -> dict:
        try:
            response = await self._client.get(endpoint, headers=headers, params=params)
        except httpx.RequestError as e:
            raise exceptions.RequestError(
                message=str(e),
            )
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise exceptions.HTTPStatusError(
                status_code=response.status_code,
                message=str(e),
            )
        return response.json()

    async def post(self, endpoint: str, headers: dict = None, json: dict = None) -> dict:
        try:
            response = await self._client.post(endpoint, headers=headers, json=json)
        except httpx.RequestError as e:
            raise exceptions.RequestError(
                message=str(e),
            )
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise exceptions.HTTPStatusError(
                status_code=response.status_code,
                message=str(e),
            )
        return response.json()

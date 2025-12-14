from abc import ABC, abstractmethod


class IApiClient(ABC):
    """Интерфейс универсального асинхронного клиента"""
    @abstractmethod
    async def get(self, endpoint: str, headers: dict = None, params: dict = None) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def post(self, endpoint: str, headers: dict = None, json: dict = None) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def patch(self, endpoint: str, headers: dict = None, json: dict = None) -> dict:
        raise NotImplementedError

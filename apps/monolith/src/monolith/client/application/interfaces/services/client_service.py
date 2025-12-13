from abc import ABC, abstractmethod

from monolith.client.application.dtos import user


class IClientService(ABC):
    """Интерфейс клиент сервиса"""
    @abstractmethod
    async def register(self, data: user.CreateUserCommand) -> user.CreateUserResponse:
        raise NotImplementedError

    @abstractmethod
    async def login(self, data: user.LoginUserCommand) -> user.LoginUserResponse:
        raise NotImplementedError

    @abstractmethod
    async def logout(self, access_token: str) -> bool:
        raise NotImplementedError

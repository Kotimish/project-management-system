from abc import ABC, abstractmethod

from monolith.client.application.dtos import user
from monolith.client.application.dtos.user_profile import GetUserProfileResponse


class IClientService(ABC):
    """Интерфейс клиент сервиса"""
    @abstractmethod
    async def register(self, data: user.CreateUserCommand) -> user.CreateUserResponse:
        """Регистрация пользователя"""
        raise NotImplementedError

    @abstractmethod
    async def login(self, data: user.LoginUserCommand) -> user.LoginUserResponse:
        """Вход пользователя в систему"""
        raise NotImplementedError

    @abstractmethod
    async def logout(self, access_token: str) -> bool:
        """Выход пользователя из системы"""
        raise NotImplementedError

    @abstractmethod
    async def get_current_user(self, access_token: str) -> GetUserProfileResponse | None:
        """Получить информацию о пользователе, отправившем запрос"""
        raise NotImplementedError

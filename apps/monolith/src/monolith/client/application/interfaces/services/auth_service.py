from abc import ABC, abstractmethod

from monolith.client.application.dtos import user
from monolith.client.application.dtos.token import TokenDTO


class IAuthService(ABC):
    """Интерфейс сервиса авторизации"""

    @abstractmethod
    async def register(self, data: user.CreateUserCommand) -> user.CreateUserResponse | None:
        """Регистрация пользователя"""
        raise NotImplementedError

    @abstractmethod
    async def login(self, data: user.LoginUserCommand) -> user.LoginUserResponse | None:
        """Вход пользователя в систему"""
        raise NotImplementedError

    @abstractmethod
    async def logout(self, refresh_token: str) -> bool:
        """Выход пользователя из системы"""
        raise NotImplementedError

    @abstractmethod
    async def validate_token(self, access_token: str) -> TokenDTO | None:
        """
        Отправляет запрос на сервис авторизации для декодирования и проверки актуальности
        токена пользователя с возвратом данных
        """
        raise NotImplementedError

from abc import ABC, abstractmethod

from monolith.auth.application.dtos.token import AccessTokenDTO
from monolith.auth.application.dtos.user import LoginUserResponse, LoginUserCommand


class IAuthenticationService(ABC):
    """Интерфейс сервиса авторизации и аутентификации пользователей"""
    @abstractmethod
    async def login_user(self, data: LoginUserCommand) -> LoginUserResponse:
        """Аутентифицирует пользователя и создаёт сессию"""
        raise NotImplementedError

    @abstractmethod
    async def logout_user(self, access_token: str) -> bool:
        """Завершает сессию пользователя"""
        raise NotImplementedError

    @abstractmethod
    async def refresh_access_token(self, refresh_token: str) -> str:
        """Обновление токена пользователя"""
        raise NotImplementedError

    @abstractmethod
    async def validate_access(self, access_token: str) -> AccessTokenDTO:
        """Декодирование и проверка на актуальность токена пользователя с возвратом данных"""
        raise NotImplementedError


from abc import ABC, abstractmethod

from monolith.user_profile.application.dtos.token import TokenDTO


class ITokenService(ABC):
    """Интерфейс сервиса проверки токена"""
    @abstractmethod
    async def validate_token(self, access_token: str) -> TokenDTO:
        """
        Отправляет запрос на сервис авторизации для декодирования и проверки актуальности
        токена пользователя с возвратом данных
        """
        raise NotImplementedError
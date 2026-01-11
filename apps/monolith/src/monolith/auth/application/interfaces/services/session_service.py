from abc import ABC, abstractmethod

from monolith.auth.domain.model.session import Session
from monolith.auth.domain.model.user import User


class ISessionService(ABC):
    """Интерфейс сервиса работы с сессиями пользователей"""
    @abstractmethod
    async def create_session(self, user: User) -> Session:
        """Создать сессию"""
        raise NotImplementedError

    @abstractmethod
    async def get_session_by_id(self, session_id: int) -> Session | None:
        """Получить сессию по ее идентификатору"""
        raise NotImplementedError

    @abstractmethod
    async def revoke_session(self, session_id: int) -> bool:
        """Деактивировать сессию"""
        raise NotImplementedError

    @abstractmethod
    async def delete_session(self, session_id: int) -> bool:
        """Удалить сессию"""
        raise NotImplementedError

from abc import ABC, abstractmethod

from monolith.auth.domain.model.session import Session


class ISessionRepository(ABC):
    """Интерфейс репозитория для сессий пользователей."""

    @abstractmethod
    async def add(self, session: Session) -> Session:
        """
        Сохраняет новую сессию пользователя.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, session_id: int) -> Session | None:
        """
        Находит сессию пользователя по ID.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[Session]:
        """
        Получает список всех сессий пользователей.
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, session_id: int, session: Session) -> Session | None:
        """
        Обновление данных сессии пользователя
        """
        raise NotImplementedError

    @abstractmethod
    async def remove(self, session_id: int) -> bool:
        """
        Удаляет сессию пользователя по ID.
        """
        raise NotImplementedError

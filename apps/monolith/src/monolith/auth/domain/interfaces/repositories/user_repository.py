from abc import ABC, abstractmethod

from monolith.auth.domain.model.user import User


class IUserRepository(ABC):
    """Интерфейс репозитория для пользователей."""

    @abstractmethod
    async def add(self, user: User) -> User:
        """
        Сохраняет нового пользователя.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, user_id: int) -> User | None:
        """
        Находит пользователя по ID.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_login(self, login: str) -> User | None:
        """
        Находит пользователя по его логину (slug).
        """
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[User]:
        """
        Получает список всех пользователей.
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, user_id: int, user: User) -> User | None:
        """
        Обновление данных пользователя
        """
        raise NotImplementedError

    @abstractmethod
    async def remove(self, user_id: int) -> bool:
        """
        Удаляет пользователя по ID.
        """
        raise NotImplementedError

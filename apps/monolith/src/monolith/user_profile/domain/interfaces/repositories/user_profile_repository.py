from abc import ABC, abstractmethod

from monolith.user_profile.domain.model.user_profile import UserProfile


class IUserProfileRepository(ABC):
    """Интерфейс репозитория для профилей пользователей."""

    @abstractmethod
    async def add(self, profile: UserProfile) -> UserProfile:
        """
        Сохраняет новый профиль пользователя.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, profile_id: int) -> UserProfile | None:
        """
        Находит профиль пользователя по ID.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_auth_user_id(self, auth_user_id: int) -> UserProfile | None:
        """
        Находит профиль пользователя по его id из сервиса авторизации.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_auth_user_ids(self, auth_user_ids: list[int]) -> list[UserProfile]:
        """
        Находит профили пользователей по их id из сервиса авторизации.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[UserProfile]:
        """
        Получает список всех профилей пользователей.
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, profile_id: int, profile: UserProfile) -> UserProfile | None:
        """
        Обновление данных профиля пользователя.
        """
        raise NotImplementedError

    @abstractmethod
    async def remove(self, profile_id: int) -> bool:
        """
        Удаляет профиль пользователя по ID.
        """
        raise NotImplementedError

from abc import ABC, abstractmethod

from monolith.auth.domain.model.role import Role


class IRoleRepository(ABC):
    """Интерфейс репозитория для ролей пользователей."""

    @abstractmethod
    async def add(self, role: Role) -> Role:
        """
        Сохраняет новую роль пользователя.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, role_id: int) -> Role | None:
        """
        Находит роль пользователя по ID.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_slug(self, slug: str) -> Role | None:
        """
        Находить роль пользователя по уникальной метки (slug)
        """
        raise NotImplementedError


    @abstractmethod
    async def get_all(self) -> list[Role]:
        """
        Получает список всех ролей пользователей.
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, role_id: int, role: Role) -> Role | None:
        """
        Обновление данных роли пользователя
        """
        raise NotImplementedError

    @abstractmethod
    async def remove(self, role_id: int) -> bool:
        """
        Удаляет роль пользователя по ID.
        """
        raise NotImplementedError

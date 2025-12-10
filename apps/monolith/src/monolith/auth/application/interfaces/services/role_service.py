from abc import ABC, abstractmethod

from monolith.auth.domain.model.role import Role


class IRoleService(ABC):
    """Интерфейс сервиса ролей пользователей"""
    @abstractmethod
    async def get_role_by_id(self, role_id) -> Role | None:
        """Получения роли по id"""
        raise NotImplementedError

    @abstractmethod
    async def get_default_role_id(self) -> int:
        """Получение идентификатора дефолтной роли пользователя"""
        raise NotImplementedError

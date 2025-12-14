from abc import ABC, abstractmethod

from monolith.project.domain.model import Project


class IProjectRepository(ABC):
    """Интерфейс репозитория для модели Проект."""

    @abstractmethod
    async def add(self, project: Project) -> Project:
        """
        Сохраняет новый Проект.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, project_id: int) -> Project | None:
        """
        Находит Проект по ID.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_owner_id(self, owner_id: int) -> list[Project]:
        """
        Находит все Проекта по ID владельца.
        """
        raise NotImplementedError


    @abstractmethod
    async def get_all(self) -> list[Project]:
        """
        Получает список всех Проектов.
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, project_id: int, project: Project) -> Project | None:
        """
        Обновление данных Проекта
        """
        raise NotImplementedError

    @abstractmethod
    async def remove(self, project_id: int) -> bool:
        """
        Удаляет Проект по ID.
        """
        raise NotImplementedError

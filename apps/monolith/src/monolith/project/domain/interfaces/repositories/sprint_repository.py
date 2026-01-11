from abc import ABC, abstractmethod

from monolith.project.domain.model import Sprint


class ISprintRepository(ABC):
    """Интерфейс репозитория для Спринта."""

    @abstractmethod
    async def add(self, sprint: Sprint) -> Sprint:
        """
        Сохраняет новый спринт проекта.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, sprint_id: int) -> Sprint | None:
        """
        Находит спринт проекта по ID.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[Sprint]:
        """
        Получает список всех спринтов.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_project_id(self, project_id: int) -> list[Sprint]:
        """
        Получает список всех спринтов определенного проекта.
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, sprint_id: int, sprint: Sprint) -> Sprint | None:
        """
        Обновление данных спринта проекта
        """
        raise NotImplementedError

    @abstractmethod
    async def remove(self, sprint_id: int) -> bool:
        """
        Удаляет спринт проекта по ID.
        """
        raise NotImplementedError

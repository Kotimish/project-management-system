from abc import ABC, abstractmethod

from monolith.project.domain.model import TaskStatus


class ITaskStatusRepository(ABC):
    """Интерфейс репозитория для статусов задач."""

    @abstractmethod
    async def add(self, task_status: TaskStatus) -> TaskStatus:
        """
        Сохраняет новый статус задачи.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, task_status_id: int) -> TaskStatus | None:
        """
        Находит статус задачи по ID.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_slug(self, slug: str) -> TaskStatus | None:
        """
        Находить статус задачи по уникальной метки (slug)
        """
        raise NotImplementedError


    @abstractmethod
    async def get_all(self) -> list[TaskStatus]:
        """
        Получает список всех статусов задач.
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, task_status_id: int, task_status: TaskStatus) -> TaskStatus | None:
        """
        Обновление данных статуса задачи
        """
        raise NotImplementedError

    @abstractmethod
    async def remove(self, task_status_id: int) -> bool:
        """
        Удаляет статус задачи по ID.
        """
        raise NotImplementedError

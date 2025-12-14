from abc import ABC, abstractmethod

from monolith.project.domain.model import TaskStatus


class ITaskStatusService(ABC):
    """Интерфейс сервиса статутов задач"""

    @abstractmethod
    async def get_all_statuses(self) -> list[TaskStatus]:
        """Получить информацию обо всех статусах задач"""
        raise NotImplementedError

    @abstractmethod
    async def get_status_by_id(self, status_id) -> TaskStatus | None:
        """Получить статус задачи по ID"""
        raise NotImplementedError

    @abstractmethod
    async def get_status_by_slug(self, slug: str) -> TaskStatus | None:
        """Получить статус задачи по уникальному тегу"""
        raise NotImplementedError

    @abstractmethod
    async def get_default_status(self) -> TaskStatus | None:
        """Получить дефолтный статус задачи"""
        raise NotImplementedError

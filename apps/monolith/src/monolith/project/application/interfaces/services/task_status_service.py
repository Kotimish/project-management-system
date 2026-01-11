from abc import ABC, abstractmethod

from monolith.project.application.dto import task_status as dto


class ITaskStatusService(ABC):
    """Интерфейс сервиса статутов задач"""

    @abstractmethod
    async def get_all_statuses(self) -> list[dto.TaskStatusDTO]:
        """Получить информацию обо всех статусах задач"""
        raise NotImplementedError

    @abstractmethod
    async def get_status_by_id(self, status_id) -> dto.TaskStatusDTO | None:
        """Получить статус задачи по ID"""
        raise NotImplementedError

    @abstractmethod
    async def get_status_by_slug(self, slug: str) -> dto.TaskStatusDTO | None:
        """Получить статус задачи по уникальному тегу"""
        raise NotImplementedError

    @abstractmethod
    async def get_default_status(self) -> dto.TaskStatusDTO | None:
        """Получить дефолтный статус задачи"""
        raise NotImplementedError

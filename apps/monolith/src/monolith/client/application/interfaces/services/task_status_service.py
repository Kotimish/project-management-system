from abc import ABC, abstractmethod

from monolith.client.application.dtos import task_status as dto


class ITaskStatusService(ABC):
    """Интерфейс сервиса статусов задач"""

    @abstractmethod
    async def get_task_statuses(self) -> list[dto.TaskStatusDTO]:
        """Получить все возможные статусы задачи"""
        raise NotImplementedError

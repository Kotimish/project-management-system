from abc import ABC, abstractmethod

from monolith.client.application.dtos import task as dto
from monolith.client.application.dtos import views as views


class ITaskService(ABC):
    """Интерфейс сервиса задач"""

    @abstractmethod
    async def get_tasks_by_auth_user_id(self, auth_user_id: int) -> views.TaskListView | None:
        """Получить все задачи пользователя"""
        raise NotImplementedError

    @abstractmethod
    async def get_task_by_id(self, project_id: int, sprint_id: int, task_id: int) -> views.TaskView | None:
        """Получить задача по id"""
        raise NotImplementedError

    @abstractmethod
    async def create_task(self, project_id: int, sprint_id: int, data: dto.CreateTaskCommand) -> dto.TaskDTO | None:
        """Создать новую задачу в спринте проекта"""
        raise NotImplementedError

    @abstractmethod
    async def update_task(
            self,
            project_id: int,
            sprint_id: int,
            task_id: int,
            data: dto.UpdateTaskCommand
    ) -> dto.TaskDTO | None:
        """Обновить данные задачи"""
        raise NotImplementedError

    @abstractmethod
    async def delete_task(self, project_id: int, sprint_id: int, task_id: int) -> None:
        """удалить задачу"""
        raise NotImplementedError

from abc import ABC, abstractmethod

from monolith.project.application.dto import task as task_dto
from monolith.project.application.dto import task as dto


class ITaskService(ABC):
    """Интерфейс сервиса задач"""

    @abstractmethod
    async def create_task(
            self,
            title: str,
            project_id: int,
            assignee_id: int | None = None,
            sprint_id: int | None = None,
            description: str | None = None
    ) -> dto.TaskDTO:
        """Создание новой задачи"""
        raise NotImplementedError

    @abstractmethod
    async def get_task_by_id(self, task_id: int) -> dto.TaskDTO:
        """Получить задачу по id"""
        raise NotImplementedError

    @abstractmethod
    async def get_list_tasks_by_project(self, project_id: int) -> list[dto.TaskDTO]:
        """Получить задачу по id проекта"""
        raise NotImplementedError

    @abstractmethod
    async def get_list_tasks_by_sprint(self, sprint_id: int) -> list[dto.TaskDTO]:
        """Получить задачу по id спринта"""
        raise NotImplementedError

    @abstractmethod
    async def get_tasks_by_auth_user_id(self, auth_user_id: int) -> list[dto.TaskDTO]:
        """Получить задачу по id пользователя"""
        raise NotImplementedError

    @abstractmethod
    async def get_tasks_by_auth_user_in_project(self, project_id: int, auth_user_id: int) -> list[dto.TaskDTO]:
        """Получить задачу по id пользователя и id проекта"""
        raise NotImplementedError

    @abstractmethod
    async def delete_task(self, task_id: int) -> bool:
        """Удалить задачу по id"""
        raise NotImplementedError

    @abstractmethod
    async def update_task(
            self,
            project_id: int,
            sprint_id: int,
            task_id: int,
            data: task_dto.UpdateTaskCommand
    ) -> dto.TaskDTO:
        """Обновить задачу"""
        raise NotImplementedError

    @abstractmethod
    async def add_task_to_sprint(self, task_id: int, sprint_id: int) -> dto.TaskDTO:
        """Добавить задачу в спринт"""
        raise NotImplementedError

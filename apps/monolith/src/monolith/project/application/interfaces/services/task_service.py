from abc import ABC, abstractmethod

from monolith.project.application.dto import task as task_dto
from monolith.project.domain.model import Task


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
    ) -> Task:
        """Создание новой задачи"""
        raise NotImplementedError

    @abstractmethod
    async def get_task_by_id(self, task_id: int) -> Task:
        """Получить задачу по id"""
        raise NotImplementedError

    @abstractmethod
    async def get_list_tasks_by_assignee_id(self, assignee_id: int) -> list[Task]:
        """Получить задачу по id ответственного"""
        raise NotImplementedError

    @abstractmethod
    async def get_list_tasks_by_project(self, project_id: int) -> list[Task]:
        """Получить задачу по id проекта"""
        raise NotImplementedError

    @abstractmethod
    async def get_list_tasks_by_sprint(self, sprint_id: int) -> list[Task]:
        """Получить задачу по id спринта"""
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
    ) -> Task:
        """Обновить задачу"""
        raise NotImplementedError

    @abstractmethod
    async def add_task_to_sprint(self, task_id: int, sprint_id: int) -> Task:
        """Добавить задачу в спринт"""
        raise NotImplementedError

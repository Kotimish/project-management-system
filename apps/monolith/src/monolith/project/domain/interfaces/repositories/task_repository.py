from abc import ABC, abstractmethod

from monolith.project.domain.model import Task, TaskView


class ITaskRepository(ABC):
    """Интерфейс репозитория для задач."""

    @abstractmethod
    async def add(self, task: Task) -> Task:
        """
        Сохраняет новую задачу.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, task_id: int) -> Task | None:
        """
        Находит задачу по ID.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[Task]:
        """
        Получает список всех задач.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_list_tasks_by_auth_user_id(self, auth_user_id: int) -> list[TaskView]:
        """Получить задачу по внешнему id пользователя"""
        raise NotImplementedError

    @abstractmethod
    async def get_list_tasks_by_project(self, project_id: int) -> list[Task]:
        """Получить задачу по id проекта"""
        raise NotImplementedError

    @abstractmethod
    async def get_list_tasks_by_sprint(self, sprint_id: int) -> list[TaskView]:
        """Получить задачу по id спринта"""
        raise NotImplementedError

    @abstractmethod
    async def update(self, task_id: int, task: Task) -> Task | None:
        """
        Обновление данных задачи
        """
        raise NotImplementedError

    @abstractmethod
    async def remove(self, task_id: int) -> bool:
        """
        Удаляет задачу по ID.
        """
        raise NotImplementedError

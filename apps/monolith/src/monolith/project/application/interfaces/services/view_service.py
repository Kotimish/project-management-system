from abc import ABC, abstractmethod

from monolith.project.application.dto import views

class IViewService(ABC):
    """Интерфейс сервиса для обработки запросов на чтение агрегат сущностей"""

    @abstractmethod
    async def get_project_detail(self, project_id: int) -> views.ProjectView:
        """Получение полной информации по проекту и связанным сущностям"""
        raise NotImplementedError

    @abstractmethod
    async def get_sprint_detail(self, project_id: int, sprint_id: int) -> views.SprintView:
        """Получение полной информации по спринту и связанным сущностям"""
        raise NotImplementedError

    @abstractmethod
    async def get_task_detail(self, project_id: int, sprint_id: int, task_id: int) -> views.TaskView:
        """Получение полной информации по задаче и связанным сущностям"""
        raise NotImplementedError

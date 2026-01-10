from abc import ABC, abstractmethod

from monolith.client.application.dtos import sprint as dto
from monolith.client.application.dtos import views as views


class ISprintService(ABC):
    """Интерфейс сервиса спринтов"""

    @abstractmethod
    async def get_sprints_by_project_id(self, project_id: int) -> list[dto.SprintDTO]:
        """Получить все спринта проекта"""
        raise NotImplementedError

    @abstractmethod
    async def get_sprint_by_id(self, project_id: int, sprint_id: int) -> views.SprintView | None:
        """Получить спринт по id"""
        raise NotImplementedError

    @abstractmethod
    async def create_sprint(self, project_id: int, data: dto.CreateSprintCommand) -> dto.SprintDTO | None:
        """Создать новый спринт в проекте"""
        raise NotImplementedError

    @abstractmethod
    async def update_sprint(self, project_id: int, sprint_id: int, data: dto.UpdateSprintCommand) -> dto.SprintDTO | None:
        """Обновить данные спринта"""
        raise NotImplementedError

    @abstractmethod
    async def delete_sprint(self, project_id: int, sprint_id: int) -> None:
        """Удалить спринт"""
        raise NotImplementedError


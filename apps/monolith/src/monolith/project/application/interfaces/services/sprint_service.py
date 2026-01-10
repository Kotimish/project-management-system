from abc import ABC, abstractmethod
from datetime import date

from monolith.project.application.dto import sprint as dto
from monolith.project.application.dto.sprint import UpdateSprintCommand


class ISprintService(ABC):
    """Интерфейс сервиса Спринта"""

    @abstractmethod
    async def create_sprint(self, name: str, project_id: int, start_date: date, end_date: date) -> dto.SprintDTO:
        """Создать новый спринт"""
        raise NotImplementedError

    @abstractmethod
    async def get_sprint_by_id(self, sprint_id: int) -> dto.SprintDTO:
        """Получить спринт по id"""
        raise NotImplementedError

    @abstractmethod
    async def get_all_sprint_by_project_id(self, project_id: int) -> list[dto.SprintDTO]:
        """Получить все спринты из проекта"""
        raise NotImplementedError

    @abstractmethod
    async def update_sprint(self, project_id: int, sprint_id: int, data: UpdateSprintCommand) -> dto.SprintDTO:
        """Обновить данные спринта"""
        raise NotImplementedError

    @abstractmethod
    async def delete_sprint(self, project_id: int, sprint_id: int) -> None:
        """Удалить спринт"""
        raise NotImplementedError

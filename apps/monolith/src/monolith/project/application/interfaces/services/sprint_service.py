from abc import ABC, abstractmethod
from datetime import date

from monolith.project.application.dto.sprint import UpdateSprintCommand
from monolith.project.domain.model import Sprint


class ISprintService(ABC):
    """Интерфейс сервиса Спринта"""

    @abstractmethod
    async def create_sprint(self, name: str, project_id: int, start_date: date, end_date: date) -> Sprint:
        """Создать новый спринт"""
        raise NotImplementedError

    @abstractmethod
    async def get_sprint_by_id(self, sprint_id: int) -> Sprint:
        """Получить спринт по id"""
        raise NotImplementedError

    @abstractmethod
    async def get_all_sprint_by_project_id(self, project_id: int) -> list[Sprint]:
        """Получить все спринты из проекта"""
        raise NotImplementedError

    @abstractmethod
    async def update_sprint(self, sprint_id: int, data: UpdateSprintCommand) -> Sprint:
        """Обновить данные спринта"""
        raise NotImplementedError

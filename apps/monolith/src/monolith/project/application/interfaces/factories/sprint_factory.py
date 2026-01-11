from abc import ABC, abstractmethod
from datetime import date

from monolith.project.domain.model import Sprint


class ISprintFactory(ABC):
    """Интерфейс фабрики спринта проекта"""

    @abstractmethod
    def create(self, name: str, project_id: int, start_date: date, end_date: date) -> Sprint:
        raise NotImplementedError

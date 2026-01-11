from abc import ABC, abstractmethod

from monolith.project.domain.model import Project


class IProjectFactory(ABC):
    """Интерфейс фабрики проекта"""
    @abstractmethod
    def create(self, name: str, owner_id: int, description: str = None) -> Project:
        raise NotImplementedError

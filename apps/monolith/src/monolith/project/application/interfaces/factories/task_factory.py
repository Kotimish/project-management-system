from abc import ABC, abstractmethod

from monolith.project.domain.model import Task


class ITaskFactory(ABC):
    """Интерфейс фабрики задач проекта"""

    @abstractmethod
    def create(
            self,
            title: str,
            project_id: int,
            status_id: int,
            assignee_id: int | None,
            description: str = None
    ) -> Task:
        raise NotImplementedError

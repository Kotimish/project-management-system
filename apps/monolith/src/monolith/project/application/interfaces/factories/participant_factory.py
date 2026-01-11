from abc import ABC, abstractmethod

from monolith.project.domain.model import Participant


class IParticipantFactory(ABC):
    """Интерфейс фабрики участников проекта"""

    @abstractmethod
    def create(self, project_id: int, user_id: int) -> Participant:
        raise NotImplementedError

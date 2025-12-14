from abc import ABC, abstractmethod

from monolith.project.domain.model import Participant


class IParticipantService(ABC):
    """Интерфейс сервиса участников проекта"""

    @abstractmethod
    async def add_participant(self, project_id: int, user_id: int) -> Participant:
        """Добавить участника в проект"""
        raise NotImplementedError

    @abstractmethod
    async def remove_participant(self, project_id: int, user_id: int) -> bool:
        """Убрать участника из проекта"""
        raise NotImplementedError

    @abstractmethod
    async def get_participants_by_project(self, project_id: int) -> list[Participant]:
        """Получить всех участников проекта"""
        raise NotImplementedError

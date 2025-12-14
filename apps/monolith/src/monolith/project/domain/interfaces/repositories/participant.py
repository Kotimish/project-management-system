from abc import ABC, abstractmethod

from monolith.project.domain.model import Participant


class IParticipantRepository(ABC):
    """Интерфейс репозитория для участников проекта."""

    @abstractmethod
    async def add(self, participant: Participant) -> Participant:
        """
        Сохраняет нового участника проекта.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, participant_id: int) -> Participant | None:
        """
        Находит участника проекта по ID.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[Participant]:
        """
        Получает список всех участников проекта.
        """
        raise NotImplementedError

    @abstractmethod
    async def remove(self, participant_id: int) -> bool:
        """
        Удаляет участника проекта по ID.
        """
        raise NotImplementedError

from abc import ABC, abstractmethod

from monolith.client.application.dtos import participant as dto


class IParticipantService(ABC):
    """Интерфейс сервиса участников проекта"""

    @abstractmethod
    async def get_participants_by_project(self, project_id: int) -> list[dto.ParticipantDTO]:
        """Получить всех участников проекта"""
        raise NotImplementedError

    @abstractmethod
    async def add_participant_to_project(self, project_id: int, user_id: int) -> dto.ParticipantDTO | None:
        """Добавить пользователя в участники проекта"""
        raise NotImplementedError

    @abstractmethod
    async def remove_participant_from_project(self, project_id: int, user_id: int) -> None:
        """Исключить пользователя из участников проекта"""
        raise NotImplementedError

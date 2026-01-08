from abc import ABC

from monolith.client.application.dtos import participant as dto


class IParticipantService(ABC):
    """Интерфейс сервиса участников проекта"""

    async def get_participants_by_project(self, project_id: int) -> list[dto.ParticipantDTO]:
        """Получить всех участников проекта"""
        raise NotImplementedError

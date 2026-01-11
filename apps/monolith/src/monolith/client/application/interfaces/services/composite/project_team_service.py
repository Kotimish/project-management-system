from abc import ABC, abstractmethod

from monolith.client.application.dtos.composite import project_team as dto


class IProjectTeamService(ABC):
    """Интерфейс агрегат сервиса участников проекта и их профилей"""

    @abstractmethod
    async def get_participants_by_project(self, project_id: int) -> list[dto.ProjectTeamDTO]:
        """Получить всех участников проекта с профилем"""
        raise NotImplementedError

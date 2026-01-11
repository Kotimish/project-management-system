from abc import ABC, abstractmethod

from monolith.project.application.dto import project as project_dto
from monolith.project.application.dto import participant as participant_dto
from monolith.project.application.dto.project import UpdateProjectCommand
from monolith.project.domain.model import Participant


class IProjectService(ABC):
    """Интерфейс сервиса проектов"""

    @abstractmethod
    async def create_project(self, name: str, owner_id: int, description: str = None) -> project_dto.ProjectDTO:
        """Создание проекта"""
        raise NotImplementedError

    @abstractmethod
    async def get_project_by_id(self, project_id: int) -> project_dto.ProjectDTO:
        """Получить проект по id"""
        raise NotImplementedError

    @abstractmethod
    async def get_list_projects_with_user(self, user_id: int) -> list[project_dto.ProjectDTO]:
        """Получить список проектов с указанным пользователем в участниках"""
        raise NotImplementedError

    @abstractmethod
    async def update_project(self, project_id: int, owner_id: int, data: UpdateProjectCommand) -> project_dto.ProjectDTO:
        """Обновить данные проекта"""
        raise NotImplementedError

    @abstractmethod
    async def delete_project(self, project_id: int, owner_id: int) -> None:
        """Удалить проект"""
        raise NotImplementedError

    @abstractmethod
    async def add_participant_to_project(self, project_id: int, owner_id: int, user_id: int) -> participant_dto.ParticipantDTO:
        """Добавить участника в проект"""
        raise NotImplementedError

    @abstractmethod
    async def remove_participant_from_project(self, project_id: int, owner_id: int, user_id: int) -> None:
        """Убрать участника из проекта"""
        raise NotImplementedError

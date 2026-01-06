from abc import ABC, abstractmethod

from monolith.project.application.dto import project as dto
from monolith.project.application.dto.project import UpdateProjectCommand
from monolith.project.domain.model import Participant


class IProjectService(ABC):
    """Интерфейс сервиса проектов"""

    @abstractmethod
    async def create_project(self, name: str, owner_id: int, description: str = None) -> dto.ProjectDTO:
        """Создание проекта"""
        raise NotImplementedError

    @abstractmethod
    async def get_project_by_id(self, project_id: int) -> dto.ProjectDTO:
        """Получить проект по id"""
        raise NotImplementedError

    @abstractmethod
    async def get_list_projects_with_user(self, user_id: int) -> list[dto.ProjectDTO]:
        """Получить список проектов с указанным пользователем в участниках"""
        raise NotImplementedError

    @abstractmethod
    async def update_project(self, project_id: int, data: UpdateProjectCommand) -> dto.ProjectDTO:
        """Обновить данные проекта"""
        raise NotImplementedError

    @abstractmethod
    async def delete_project(self, project_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def add_participant_to_project(self, project_id: int, user_id: int) -> Participant:
        """Добавить участника в проект"""
        raise NotImplementedError

    @abstractmethod
    async def remove_participant_from_project(self, project_id: int, user_id: int) -> bool:
        """Убрать участника из проекта"""
        raise NotImplementedError

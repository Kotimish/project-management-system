from abc import ABC, abstractmethod

from monolith.client.application.dtos import project as dto
from monolith.client.application.dtos import views as views


class IProjectService(ABC):
    """Интерфейс сервиса проектов"""

    @abstractmethod
    async def get_project_by_id(self, project_id: int) -> views.ProjectView | None:
        """Получить подробности об проекте по его id"""
        raise NotImplementedError

    @abstractmethod
    async def get_projects_by_user_id(self, user_id) -> list[dto.ProjectDTO]:
        """Получить список проектов с определенным участником по его id из сервиса авторизации"""
        raise NotImplementedError

    @abstractmethod
    async def create_project(self, data: dto.CreateProjectDTO) -> dto.ProjectDTO | None:
        """Создать новый проект"""
        raise NotImplementedError

    @abstractmethod
    async def update_project(
            self,
            project_id: int,
            data: dto.UpdateProjectDTO,
            access_token: str
    ) -> dto.ProjectDTO | None:
        """Обновить данные проекта"""
        raise NotImplementedError

    @abstractmethod
    async def delete_project(self, project_id: int, access_token: str) -> None:
        """Удалить проект"""
        raise NotImplementedError

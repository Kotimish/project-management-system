from monolith.client.application.dtos import project as dto
from monolith.client.application.dtos import views as views
from monolith.client.application.exceptions import api_client_exception as exceptions
from monolith.client.application.interfaces.client import IApiClient
from monolith.client.application.interfaces.services.project_service import IProjectService


class ProjectService(IProjectService):
    """Сервис проектов"""

    def __init__(self, project_client: IApiClient):
        self.project_client = project_client

    async def get_project_by_id(self, project_id: int) -> views.ProjectView | None:
        try:
            raw_project = await self.project_client.get(
                f"/api/projects/{project_id}",
            )
            project = views.ProjectView.model_validate(raw_project)
            return project
        except exceptions.HTTPStatusError:
            return None

    async def get_projects_by_user_id(self, user_id: int) -> list[dto.ProjectDTO]:
        try:
            raw_projects = await self.project_client.get(
                f"/api/projects/search?user_id={user_id}",
            )
            projects = [
                dto.ProjectDTO.model_validate(raw_project)
                for raw_project in raw_projects
            ]
            return projects
        except exceptions.HTTPStatusError:
            return []

    async def create_project(self, data: dto.CreateProjectDTO) -> dto.ProjectDTO | None:
        try:
            raw_project = await self.project_client.post(
                "/api/projects/",
                json=data.model_dump(mode='json')
            )
            project = dto.ProjectDTO.model_validate(raw_project)
            return project
        except exceptions.HTTPStatusError:
            return None

    async def update_project(self, project_id: int, data: dto.UpdateProjectDTO) -> dto.ProjectDTO | None:
        try:
            raw_project = await self.project_client.patch(
                f"/api/projects/{project_id}",
                json=data.model_dump(mode='json')
            )
            project = dto.ProjectDTO.model_validate(raw_project)
            return project
        except exceptions.HTTPStatusError:
            return None

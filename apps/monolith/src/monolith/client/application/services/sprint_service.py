from monolith.client.application.dtos import sprint as dto
from monolith.client.application.dtos import views as views
from monolith.client.application.exceptions import api_client_exception as api_exceptions
from monolith.client.application.exceptions import sprint_exception as exceptions
from monolith.client.application.interfaces.client import IApiClient
from monolith.client.application.interfaces.services.sprint_service import ISprintService


class SprintService(ISprintService):
    """Сервис спринтов"""

    def __init__(self, project_client: IApiClient):
        self.project_client = project_client

    async def get_sprints_by_project_id(self, project_id: int) -> list[dto.SprintDTO]:
        try:
            raw_sprints = await self.project_client.get(
                f"/api/projects/{project_id}/sprints/",
            )
            sprints = [
                dto.SprintDTO.model_validate(raw_project)
                for raw_project in raw_sprints
            ]
            return sprints
        except api_exceptions.HTTPStatusError:
            return []

    async def get_sprint_by_id(self, project_id: int, sprint_id: int) -> views.SprintView | None:
        try:
            raw_sprint = await self.project_client.get(
                f"/api/projects/{project_id}/sprints/{sprint_id}",
            )
            sprint = views.SprintView.model_validate(raw_sprint)
            return sprint
        except api_exceptions.HTTPStatusError:
            return None

    async def create_sprint(self, project_id: int, data: dto.CreateSprintCommand) -> dto.SprintDTO | None:
        try:
            raw_sprint = await self.project_client.post(
                f"/api/projects/{project_id}/sprints/",
                json=data.model_dump(mode='json')
            )
            sprint = dto.SprintDTO.model_validate(raw_sprint)
            return sprint
        except api_exceptions.HTTPStatusError:
            return None

    async def update_sprint(self, project_id: int, sprint_id: int,
                            data: dto.UpdateSprintCommand) -> dto.SprintDTO | None:
        try:
            raw_sprint = await self.project_client.patch(
                f"/api/projects/{project_id}/sprints/{sprint_id}",
                json=data.model_dump(mode='json')
            )
            sprint = dto.SprintDTO.model_validate(raw_sprint)
            return sprint
        except api_exceptions.HTTPStatusError:
            return None

    async def delete_sprint(self, project_id: int, sprint_id: int) -> None:
        try:
            await self.project_client.delete(
                f"/api/projects/{project_id}/sprints/{sprint_id}",
            )
        except api_exceptions.HTTPStatusError as exception:
            if exception.status_code == 409:
                raise exceptions.SprintCannotBeDeletedException(
                    "Sprint has tasks in the project"
                )
            if exception.status_code == 404:
                raise exceptions.SprintNotFoundError(
                    "Sprint not found in the project"
                )

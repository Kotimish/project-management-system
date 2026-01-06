from monolith.client.application.dtos import task_status as dto
from monolith.client.application.interfaces.client import IApiClient
from monolith.client.application.interfaces.services.task_status_service import ITaskStatusService
from monolith.client.application.exceptions import api_client_exception as exceptions


class TaskStatusService(ITaskStatusService):
    """Реализация сервиса статусов задач"""

    def __init__(self, project_client: IApiClient):
        self.project_client = project_client

    async def get_task_statuses(self) -> list[dto.TaskStatusDTO]:
        try:
            raw_statuses = await self.project_client.get(
                f"/api/task_status/",
            )
            tasks = [
                dto.TaskStatusDTO.model_validate(raw_status)
                for raw_status in raw_statuses
            ]
            return tasks
        except exceptions.HTTPStatusError:
            return []

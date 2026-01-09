from monolith.client.application.dtos import task as dto
from monolith.client.application.dtos import views as views
from monolith.client.application.exceptions import api_client_exception as exceptions
from monolith.client.application.interfaces.client import IApiClient
from monolith.client.application.interfaces.services.task_service import ITaskService


class TaskService(ITaskService):
    """Интерфейс сервиса задач"""

    def __init__(self, project_client: IApiClient):
        self.project_client = project_client

    async def get_tasks_by_auth_user_id(self, auth_user_id: int) -> views.TaskListView | None:
        try:
            raw_tasks = await self.project_client.get(
                f"/api/tasks/by_auth_user_id/{auth_user_id}",
            )
            tasks = views.TaskListView.model_validate(raw_tasks)
            return tasks
        except exceptions.HTTPStatusError:
            return None

    async def get_task_by_id(self, project_id: int, sprint_id: int, task_id: int) -> views.TaskView | None:
        try:
            raw_task = await self.project_client.get(
                f"/api/projects/{project_id}/sprints/{sprint_id}/tasks/{task_id}",
            )
            task = views.TaskView.model_validate(raw_task)
            return task
        except exceptions.HTTPStatusError:
            return None

    async def create_task(self, project_id: int, sprint_id: int, data: dto.CreateTaskCommand) -> dto.TaskDTO | None:
        try:
            raw_task = await self.project_client.post(
                f"/api/projects/{project_id}/sprints/{sprint_id}/tasks/",
                json=data.model_dump(mode='json')
            )
            task = dto.TaskDTO.model_validate(raw_task)
            return task
        except exceptions.HTTPStatusError:
            return None

    async def update_task(
            self,
            project_id: int,
            sprint_id: int,
            task_id: int,
            data: dto.UpdateTaskCommand
    ) -> dto.TaskDTO | None:
        try:
            raw_task = await self.project_client.patch(
                f"/api/projects/{project_id}/sprints/{sprint_id}/tasks/{task_id}",
                json=data.model_dump(mode='json')
            )
            task = dto.TaskDTO.model_validate(raw_task)
            return task
        except exceptions.HTTPStatusError:
            return None

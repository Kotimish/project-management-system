from monolith.project.application.dto import task as task_dto
from monolith.project.application.interfaces.factories.task_factory import ITaskFactory
from monolith.project.application.interfaces.services.task_service import ITaskService
from monolith.project.application.interfaces.services.task_status_service import ITaskStatusService
from monolith.project.domain.exceptions.task_exception import TaskNotFoundError, TaskUnauthorizedError
from monolith.project.domain.interfaces.repositories.task_repository import ITaskRepository
from monolith.project.domain.model import Task


class TaskService(ITaskService):
    """Реализация сервиса задач"""

    def __init__(
            self,
            task_status_service: ITaskStatusService,
            factory: ITaskFactory,
            repository: ITaskRepository
    ):
        self.task_status_service = task_status_service
        self.factory = factory
        self.repository = repository

    async def create_task(
            self,
            title: str,
            project_id: int,
            assignee_id: int | None = None,
            sprint_id: int | None = None,
            description: str | None = None
    ) -> Task:
        status = await self.task_status_service.get_default_status()
        task = self.factory.create(title, project_id, status.id, assignee_id, sprint_id, description)
        task = await self.repository.add(task)
        return task

    async def get_task_by_id(self, task_id: int) -> Task:
        return await self.repository.get_by_id(task_id)

    async def get_list_tasks_by_assignee_id(self, assignee_id: int) -> list[Task]:
        return await self.repository.get_list_tasks_by_assignee(assignee_id)

    async def get_list_tasks_by_project(self, project_id: int) -> list[Task]:
        return await self.repository.get_list_tasks_by_project(project_id)

    async def get_list_tasks_by_sprint(self, sprint_id: int) -> list[Task]:
        return await self.repository.get_list_tasks_by_sprint(sprint_id)

    async def delete_task(self, task_id: int) -> bool:
        return await self.repository.remove(task_id)

    async def update_task(
            self,
            project_id: int,
            sprint_id: int,
            task_id: int,
            data: task_dto.UpdateTaskCommand
    ) -> Task:
        task = await self.repository.get_by_id(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task with id \"{project_id}\" not found")
        if task.sprint_id != sprint_id:
            raise TaskUnauthorizedError("Task does not belong to sprint")
        if task.project_id != project_id:
            raise TaskUnauthorizedError("Task does not belong to project")

        if data.status_id is not None:
            task.status_id = data.status_id
        if data.assignee_id is not None:
            task.assignee_id = data.assignee_id
        if data.sprint_id is not None:
            task.sprint_id = data.sprint_id
        if data.description is not None:
            task.description = data.description
        task.touch()
        task = await self.repository.update(task_id, task)
        return task

    async def add_task_to_sprint(self, task_id: int, sprint_id: int) -> Task:
        task = await self.repository.get_by_id(task_id)
        task.sprint_id = sprint_id
        task = await self.repository.update(task_id, task)
        return task

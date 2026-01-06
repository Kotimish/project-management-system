from monolith.project.application.dto import views
from monolith.project.application.interfaces.services.view_service import IViewService
# Исключения
from monolith.project.domain.exceptions.project_exception import ProjectNotFoundError
from monolith.project.domain.exceptions.sprint_exception import SprintNotFoundError, SprintUnauthorizedError
from monolith.project.domain.exceptions.task_exception import TaskNotFoundError, TaskUnauthorizedError
from monolith.project.domain.exceptions.task_status_exception import TaskStatusNotFoundError
# Репозитории
from monolith.project.domain.interfaces.repositories.participant import IParticipantRepository
from monolith.project.domain.interfaces.repositories.project_repository import IProjectRepository
from monolith.project.domain.interfaces.repositories.sprint_repository import ISprintRepository
from monolith.project.domain.interfaces.repositories.task_repository import ITaskRepository
from monolith.project.domain.interfaces.repositories.task_status_repository import ITaskStatusRepository
from monolith.project.infrastructure.constants import COMPLETED_STATUS_SLUG


class ViewService(IViewService):
    """
    Сервис для обработки запросов на чтение агрегат сущностей.

    Примечание: реализация не оптимальна и сделана в рамках MVP.
    """

    def __init__(
            self,
            project_repository: IProjectRepository,
            sprint_repository: ISprintRepository,
            task_repository: ITaskRepository,
            task_status_repository: ITaskStatusRepository,
            participant_repository: IParticipantRepository
    ):
        self.project_repository = project_repository
        self.sprint_repository = sprint_repository
        self.task_repository = task_repository
        self.task_status_repository = task_status_repository
        self.participant_repository = participant_repository

    async def _get_dto_tasks_with_status_by_sprint_id(self, sprint_id: int) -> list[views.TaskWithStatusDetail]:
        tasks = await self.task_repository.get_list_tasks_by_sprint(sprint_id)
        dto_tasks = []
        for task in tasks:
            if task.status is None:
                raise TaskStatusNotFoundError(f"Task with id \"{task.id}\" don't have status")
            dto_status = views.TaskStatusReference(
                id=task.status.id,
                name=task.status.name,
                slug=task.status.slug
            )
            dto_task = views.TaskWithStatusDetail(
                id=task.id,
                title=task.title,
                status=dto_status
            )
            dto_tasks.append(dto_task)
        return dto_tasks

    async def _get_dto_project_reference_by_id(self, project_id: int) -> views.ProjectReference:
        project = await self.project_repository.get_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError(f"Project with id \"{project_id}\" not found")
        return views.ProjectReference(
            id=project.id,
            name=project.name,
        )

    async def get_project_detail(self, project_id: int) -> views.ProjectView:
        project = await self.project_repository.get_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError(f"Project with id \"{project_id}\" not found")
        sprints = await self.sprint_repository.get_all_by_project_id(project_id)
        dto_sprints = []
        for sprint in sprints:
            dto_tasks = await self._get_dto_tasks_with_status_by_sprint_id(sprint.id)
            total_tasks = len(dto_tasks)
            completed_tasks = sum(task.status.slug == COMPLETED_STATUS_SLUG for task in dto_tasks)
            dto_sprint = views.SprintWithTaskDetail(
                id=sprint.id,
                name=sprint.name,
                start_date=sprint.start_date,
                end_date=sprint.end_date,
                total_tasks=total_tasks,
                completed_tasks=completed_tasks,
                created_at=sprint.created_at,
                updated_at=sprint.updated_at
            )
            dto_sprints.append(dto_sprint)

        dto_project = views.ProjectDetail(
            id=project.id,
            owner_id=project.owner_id,
            name=project.name,
            description=project.description,
            created_at=project.created_at,
            updated_at=project.updated_at
        )
        return views.ProjectView(
            project=dto_project,
            sprints=dto_sprints
        )

    async def get_sprint_detail(self, project_id: int, sprint_id: int) -> views.SprintView:
        sprint = await self.sprint_repository.get_by_id(sprint_id)
        if sprint is None:
            raise SprintNotFoundError(f"Sprint with id \"{sprint_id}\" not found")
        if sprint.project_id != project_id:
            raise SprintUnauthorizedError("Sprint does not belong to project")
        dto_tasks = await self._get_dto_tasks_with_status_by_sprint_id(sprint.id)
        total_tasks = len(dto_tasks)
        completed_tasks = sum(task.status.slug == COMPLETED_STATUS_SLUG for task in dto_tasks)

        dto_project = await self._get_dto_project_reference_by_id(project_id)
        dto_sprint = views.SprintWithTaskDetail(
            id=sprint.id,
            name=sprint.name,
            start_date=sprint.start_date,
            end_date=sprint.end_date,
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            created_at=sprint.created_at,
            updated_at=sprint.updated_at
        )
        return views.SprintView(
            project=dto_project,
            sprint=dto_sprint,
            tasks=dto_tasks
        )

    async def get_task_detail(self, project_id: int, sprint_id: int, task_id: int) -> views.TaskView:
        sprint = await self.sprint_repository.get_by_id(sprint_id)
        if sprint is None:
            raise SprintNotFoundError(f"Sprint with id \"{sprint_id}\" not found")
        if sprint.project_id != project_id:
            raise SprintUnauthorizedError("Sprint does not belong to project")
        task = await self.task_repository.get_by_id(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task with id \"{project_id}\" not found")
        if task.sprint_id != sprint_id:
            raise TaskUnauthorizedError("Task does not belong to sprint")

        dto_project = await self._get_dto_project_reference_by_id(project_id)
        dto_sprint = views.SprintReference(
            id=sprint.id,
            name=sprint.name,
        )

        status = await self.task_status_repository.get_by_id(task.status_id)
        if status is None:
            raise TaskStatusNotFoundError(f"Task Status with id \"{task.status_id}\" not found")
        dto_status = views.TaskStatusReference(
            id=status.id,
            name=status.name,
            slug=status.slug
        )
        dto_task = views.TaskDetail(
            id=task.id,
            assignee_id=task.assignee_id,
            title=task.title,
            description=task.description,
            status=dto_status,
            created_at=task.created_at,
            updated_at=task.updated_at
        )

        return views.TaskView(
            project=dto_project,
            sprint=dto_sprint,
            task=dto_task
        )

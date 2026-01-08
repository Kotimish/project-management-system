from monolith.client.application.interfaces.client import IApiClient
from monolith.client.application.interfaces.services.participant_service import IParticipantService
from monolith.client.application.interfaces.services.project_service import IProjectService
from monolith.client.application.interfaces.services.sprint_service import ISprintService
from monolith.client.application.interfaces.services.task_service import ITaskService
from monolith.client.application.interfaces.services.task_status_service import ITaskStatusService
from monolith.client.application.services.participant_service import ParticipantService
from monolith.client.application.services.project_service import ProjectService
from monolith.client.application.services.sprint_service import SprintService
from monolith.client.application.services.task_service import TaskService
from monolith.client.application.services.task_status_service import TaskStatusService
from monolith.client.infrastructure.clients.http_client import HttpxApiClient
from monolith.config.settings import settings


def get_project_api_client() -> IApiClient:
    return HttpxApiClient(
        url=str(settings.urls.project_service)
    )


def get_project_service() -> IProjectService:
    project_client = get_project_api_client()
    return ProjectService(
        project_client=project_client,
    )


def get_sprint_service() -> ISprintService:
    project_client = get_project_api_client()
    return SprintService(
        project_client=project_client,
    )


def get_task_service() -> ITaskService:
    project_client = get_project_api_client()
    return TaskService(
        project_client=project_client,
    )


def get_task_status_service() -> ITaskStatusService:
    project_client = get_project_api_client()
    return TaskStatusService(
        project_client=project_client,
    )


def get_participant_service() -> IParticipantService:
    project_client = get_project_api_client()
    return ParticipantService(
        project_client=project_client,
    )

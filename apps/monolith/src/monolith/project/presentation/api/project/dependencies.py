from fastapi import Depends

from monolith.project.application.interfaces.services.project_service import IProjectService
from monolith.project.application.services.project_service import ProjectService
from monolith.project.infrastructure.factories.project_factory import ProjectFactory
from monolith.project.presentation.api.dependencies import get_project_repository
from monolith.project.presentation.api.participant.dependencies import get_participant_service
from monolith.project.presentation.api.task.dependencies import get_task_service


def get_project_service(
        repository=Depends(get_project_repository),
        participant_service=Depends(get_participant_service),
        task_service=Depends(get_task_service)
) -> IProjectService:
    factory = ProjectFactory()
    return ProjectService(
        repository=repository,
        factory=factory,
        participant_service=participant_service,
        task_service=task_service
    )

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import AsyncGenerator

from monolith.infrastructure.database import async_session
from monolith.project.application.interfaces.services.participant_service import IParticipantService
from monolith.project.application.interfaces.services.project_service import IProjectService
from monolith.project.application.interfaces.services.sprint_service import ISprintService
from monolith.project.application.interfaces.services.task_service import ITaskService
from monolith.project.application.interfaces.services.task_status_service import ITaskStatusService
from monolith.project.application.interfaces.services.view_service import IViewService
from monolith.project.application.services.participant_service import ParticipantService
from monolith.project.application.services.project_service import ProjectService
from monolith.project.application.services.sprint_service import SprintService
from monolith.project.application.services.task_service import TaskService
from monolith.project.application.services.task_status_service import TaskStatusService
from monolith.project.application.services.view_service import ViewService
from monolith.project.domain.interfaces.repositories.participant import IParticipantRepository
from monolith.project.domain.interfaces.repositories.project_repository import IProjectRepository
from monolith.project.domain.interfaces.repositories.sprint_repository import ISprintRepository
from monolith.project.domain.interfaces.repositories.task_repository import ITaskRepository
from monolith.project.domain.interfaces.repositories.task_status_repository import ITaskStatusRepository
from monolith.project.infrastructure.factories.participant_factory import ParticipantFactory
from monolith.project.infrastructure.factories.project_factory import ProjectFactory
from monolith.project.infrastructure.factories.sprint_factory import SprintFactory
from monolith.project.infrastructure.factories.task_factory import TaskFactory
from monolith.project.infrastructure.repositories.participant.orm_repository import ParticipantRepository
from monolith.project.infrastructure.repositories.project.orm_repository import ProjectRepository
from monolith.project.infrastructure.repositories.sprint.orm_repository import SprintRepository
from monolith.project.infrastructure.repositories.task.orm_repository import TaskRepository
from monolith.project.infrastructure.repositories.task_status.orm_repository import TaskStatusRepository


async def get_async_session() -> AsyncGenerator[AsyncSession]:
    async with async_session() as session:
        yield session


async def get_participant_repository(
        session: AsyncSession = Depends(get_async_session)
) -> IParticipantRepository:
    return ParticipantRepository(session)


async def get_project_repository(
        session: AsyncSession = Depends(get_async_session)
) -> IProjectRepository:
    return ProjectRepository(session)


async def get_sprint_repository(
        session: AsyncSession = Depends(get_async_session)
) -> ISprintRepository:
    return SprintRepository(session)


async def get_task_repository(
        session: AsyncSession = Depends(get_async_session)
) -> ITaskRepository:
    return TaskRepository(session)


async def get_task_status_repository(
        session: AsyncSession = Depends(get_async_session)
) -> ITaskStatusRepository:
    return TaskStatusRepository(session)


def get_participant_service(
        repository=Depends(get_participant_repository)
) -> IParticipantService:
    factory = ParticipantFactory()
    return ParticipantService(
        repository=repository,
        factory=factory
    )


def get_project_service(
        repository=Depends(get_project_repository),
        participant_service=Depends(get_participant_service)
) -> IProjectService:
    factory = ProjectFactory()
    return ProjectService(
        repository=repository,
        factory=factory,
        participant_service=participant_service
    )


def get_sprint_service(
        repository=Depends(get_sprint_repository)
) -> ISprintService:
    factory = SprintFactory()
    return SprintService(
        repository=repository,
        factory=factory
    )


def get_task_status_service(
        repository=Depends(get_task_status_repository)
) -> ITaskStatusService:
    return TaskStatusService(
        repository=repository
    )


def get_task_service(
        repository=Depends(get_task_repository),
        task_status_service=Depends(get_task_status_service)
) -> ITaskService:
    factory = TaskFactory()
    return TaskService(
        repository=repository,
        factory=factory,
        task_status_service=task_status_service
    )


def get_view_service(
        project_repository=Depends(get_project_repository),
        sprint_repository=Depends(get_sprint_repository),
        task_repository=Depends(get_task_repository),
        task_status_repository=Depends(get_task_status_repository),
        participant_repository=Depends(get_participant_repository)
) -> IViewService:
    return ViewService(
        project_repository=project_repository,
        sprint_repository=sprint_repository,
        task_repository=task_repository,
        task_status_repository=task_status_repository,
        participant_repository=participant_repository
    )

from fastapi import APIRouter, Depends, Query, HTTPException

from monolith.client.presentation.schemas import views as views
from monolith.project.application.dto.project import UpdateProjectCommand
from monolith.project.application.interfaces.services.project_service import IProjectService
from monolith.project.application.interfaces.services.view_service import IViewService
from monolith.project.domain.exceptions import project_exception as exceptions
from monolith.project.presentation.api.dependencies import get_view_service
from monolith.project.presentation.api.project.dependencies import get_project_service
from monolith.project.presentation.schemas.project import ProjectSchema, CreateProjectSchema, UpdateProjectSchema

router = APIRouter(
    prefix="/projects",
    tags=["projects"]
)


@router.get("/search")
async def search_projects(
        user_id: int | None = Query(None),
        service: IProjectService = Depends(get_project_service)
):
    projects = []
    if user_id is not None:
        projects = await service.get_list_projects_with_user(user_id)

    return [
        ProjectSchema(**project.model_dump())
        for project in projects
    ]


@router.post("/")
async def create_project(
        data: CreateProjectSchema,
        service: IProjectService = Depends(get_project_service)
) -> ProjectSchema:
    project = await service.create_project(
        name=data.name,
        owner_id=data.owner_id,
        description=data.description,
    )
    return ProjectSchema(**project.model_dump())


@router.get("/{project_id}")
async def get_project(
        project_id: int,
        service: IViewService = Depends(get_view_service)
) -> views.ProjectView:
    project = await service.get_project_detail(project_id)
    return views.ProjectView(**project.model_dump())


@router.patch("/{project_id}")
async def update_project(
        project_id: int,
        data: UpdateProjectSchema,
        service: IProjectService = Depends(get_project_service)
) -> ProjectSchema:
    command = UpdateProjectCommand(
        name=data.name,
        description=data.description
    )
    project = await service.update_project(
        project_id,
        command
    )
    return ProjectSchema(**project.model_dump())


@router.delete("/{project_id}")
async def delete_project(
        project_id: int,
        project_service: IProjectService = Depends(get_project_service)
):
    try:
        await project_service.delete_project(project_id)
    except exceptions.ProjectCannotBeDeletedException as e:
        raise HTTPException(status_code=409, detail=str(e))
    except exceptions.ProjectNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

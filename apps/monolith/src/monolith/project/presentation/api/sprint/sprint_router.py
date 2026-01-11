from fastapi import APIRouter, Depends, HTTPException

from monolith.project.application.dto.sprint import UpdateSprintCommand
from monolith.project.application.interfaces.services.sprint_service import ISprintService
from monolith.project.application.interfaces.services.view_service import IViewService
from monolith.project.domain.exceptions import sprint_exception as exceptions
from monolith.project.presentation.api.dependencies import get_view_service
from monolith.project.presentation.api.sprint.dependencies import get_sprint_service
from monolith.project.presentation.schemas.sprint import CreateSprintRequest, SprintResponse, UpdateSprintRequest
from monolith.project.presentation.schemas.views import SprintView

router = APIRouter(
    prefix="/projects/{project_id}/sprints",
    tags=["sprints"]
)


@router.get("/", response_model=list[SprintResponse])
async def get_sprints(
        project_id: int,
        service: ISprintService = Depends(get_sprint_service)
) -> list[SprintResponse]:
    sprints = []
    if project_id is not None:
        sprints = await service.get_all_sprint_by_project_id(project_id)
    # Преобразование в DTO
    return [
        SprintResponse(**sprint.model_dump())
        for sprint in sprints
    ]


@router.post("/", response_model=SprintResponse)
async def create_sprint(
        project_id: int,
        data: CreateSprintRequest,
        service: ISprintService = Depends(get_sprint_service)
) -> SprintResponse:
    sprint = await service.create_sprint(
        name=data.name,
        project_id=project_id,
        start_date=data.start_date,
        end_date=data.end_date,
    )
    return SprintResponse(**sprint.model_dump())


@router.get("/{sprint_id}", response_model=SprintView)
async def get_sprint(
        project_id: int,
        sprint_id: int,
        service: IViewService = Depends(get_view_service)
) -> SprintView:
    sprint = await service.get_sprint_detail(project_id, sprint_id)
    return SprintView(**sprint.model_dump())


@router.patch("/{sprint_id}", response_model=SprintResponse)
async def update_sprint(
        project_id: int,
        sprint_id: int,
        data: UpdateSprintRequest,
        service: ISprintService = Depends(get_sprint_service)
) -> SprintResponse:
    command = UpdateSprintCommand(
        name=data.name,
        start_date=data.start_date,
        end_date=data.end_date,
    )
    sprint = await service.update_sprint(project_id, sprint_id, command)
    return SprintResponse(**sprint.model_dump())


@router.delete("/{sprint_id}")
async def delete_sprint(
        project_id: int,
        sprint_id: int,
        sprint_service: ISprintService = Depends(get_sprint_service)
):
    try:
        await sprint_service.delete_sprint(project_id, sprint_id)
    except exceptions.SprintCannotBeDeletedException as e:
        raise HTTPException(status_code=409, detail=str(e))
    except exceptions.SprintNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

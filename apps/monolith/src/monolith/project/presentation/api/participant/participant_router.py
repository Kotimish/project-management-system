from fastapi import APIRouter, Depends

from monolith.project.application.interfaces.services.participant_service import IParticipantService
from monolith.project.presentation.api.dependencies import get_participant_service
from monolith.project.presentation.schemas import participant as schemas

router = APIRouter(
    tags=["participant"]
)


@router.get("/projects/{project_id}/participants")
async def get_participants_by_project_id(
        project_id: int,
        service: IParticipantService = Depends(get_participant_service)
):
    participants = await service.get_participants_by_project(project_id)
    return [
        schemas.ParticipantSchema(**participant.model_dump())
        for participant in participants
    ]


@router.post("/projects/{project_id}/participants")
async def add_participant(
        project_id: int,
        service: IParticipantService = Depends(get_participant_service)
):
    pass


@router.delete("/projects/{project_id}/participants/{user_id}")
async def delete_participant(
        project_id: int,
        user_id: int,
        service: IParticipantService = Depends(get_participant_service)
):
    pass

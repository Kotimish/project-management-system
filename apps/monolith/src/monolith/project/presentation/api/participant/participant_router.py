from fastapi import APIRouter, Depends

from monolith.project.application.interfaces.services.participant_service import IParticipantService
from monolith.project.presentation.api.dependencies import get_participant_service

router = APIRouter(
    tags=["participant"]
)


@router.get("/projects/{project_id}/participants")
async def get_participants(
        project_id: int,
        service: IParticipantService = Depends(get_participant_service)
):
    pass


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

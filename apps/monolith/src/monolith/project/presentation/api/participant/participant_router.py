from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from monolith.project.application.interfaces.services.participant_service import IParticipantService
from monolith.project.application.interfaces.services.project_service import IProjectService
from monolith.project.application.interfaces.services.token_service import ITokenService
from monolith.project.presentation.api.dependencies import get_token_service
from monolith.project.presentation.api.participant.dependencies import get_participant_service
from monolith.project.presentation.api.project.dependencies import get_project_service
from monolith.project.presentation.schemas import participant as schemas
from monolith.project.domain.exceptions import participant_exception as exceptions
from monolith.project.domain.exceptions import project_exception

router = APIRouter(
    tags=["participant"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


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


@router.post("/projects/{project_id}/participants/{user_id}")
async def add_participant(
        project_id: int,
        user_id: int,
        access_token: Annotated[str, Depends(oauth2_scheme)],
        project_service: IProjectService = Depends(get_project_service),
        token_service: ITokenService = Depends(get_token_service),
):
    token = await token_service.validate_token(access_token)
    if token is None:
        raise HTTPException(status_code=403, detail="Invalid token")
    try:
        participant = await project_service.add_participant_to_project(project_id, token.sub, user_id)
        return schemas.ParticipantSchema.model_validate(participant.model_dump())
    except project_exception.ProjectForbiddenError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.delete("/projects/{project_id}/participants/{user_id}")
async def delete_participant(
        project_id: int,
        user_id: int,
        access_token: Annotated[str, Depends(oauth2_scheme)],
        project_service: IProjectService = Depends(get_project_service),
        token_service: ITokenService = Depends(get_token_service),
):
    token = await token_service.validate_token(access_token)
    if token is None:
        raise HTTPException(status_code=403, detail="Invalid token")
    try:
        await project_service.remove_participant_from_project(project_id, token.sub, user_id)
    except exceptions.ParticipantCannotBeDeletedException as e:
        raise HTTPException(status_code=409, detail=str(e))
    except exceptions.ParticipantNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except project_exception.ProjectForbiddenError as e:
        raise HTTPException(status_code=403, detail=str(e))

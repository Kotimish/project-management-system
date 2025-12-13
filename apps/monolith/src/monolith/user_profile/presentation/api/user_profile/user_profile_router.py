from fastapi import APIRouter, Depends

from monolith.user_profile.application.dtos import user_profile as dto
from monolith.user_profile.application.interfaces.services import IUserProfileService
from monolith.user_profile.presentation.api.dependencies import get_user_profile_service
from monolith.user_profile.presentation.schemas import user_profile as schemas

router = APIRouter(
    prefix="/user_profile",
    tags=["user profile"]
)


@router.get("/{user_id}", response_model=schemas.GetUserProfileResponse)
async def get_user_profile(
        user_id: int,
        service: IUserProfileService = Depends(get_user_profile_service)
):
    user = await service.get_profile_by_id(user_id)
    return schemas.GetUserProfileResponse(**user.model_dump())


@router.post("/", response_model=schemas.CreateUserProfileResponse)
async def create_profile(
        data: schemas.CreateUserProfileRequest,
        service: IUserProfileService = Depends(get_user_profile_service)
):
    dto_data = dto.CreateUserProfileCommand(**data.model_dump())
    dto_response = await service.create_profile(dto_data)
    return schemas.CreateUserProfileResponse(**dto_response.model_dump())


@router.post("/{user_id}", response_model=schemas.UpdateUserProfileResponse)
async def update_user_profile(
        user_id: int,
        data: schemas.UpdateUserProfileRequest,
        service: IUserProfileService = Depends(get_user_profile_service)
):
    dto_data = dto.UpdateUserProfileCommand(**data.model_dump())
    dto_response = await service.update_profile(user_id, dto_data)
    return schemas.UpdateUserProfileResponse(**dto_response.model_dump())

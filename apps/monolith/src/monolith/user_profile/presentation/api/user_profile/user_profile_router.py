from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from monolith.user_profile.application.dtos import user_profile as dto
from monolith.user_profile.application.interfaces.services import IUserProfileService
from monolith.user_profile.application.interfaces.services.token_service import ITokenService
from monolith.user_profile.presentation.api.dependencies import get_user_profile_service, get_token_service
from monolith.user_profile.presentation.schemas import user_profile as schemas

router = APIRouter(
    prefix="/user_profile",
    tags=["user profile"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.get("/", response_model=list[schemas.GetUserProfileResponse])
async def get_all_profiles(
        service: IUserProfileService = Depends(get_user_profile_service)
):
    profiles = await service.get_all_profiles()
    return [
        schemas.GetUserProfileResponse.model_validate(profile.model_dump())
        for profile in profiles
    ]


@router.get("/{user_id}", response_model=schemas.GetUserProfileResponse)
async def get_user_profile_by_id(
        user_id: int,
        service: IUserProfileService = Depends(get_user_profile_service)
):
    profile = await service.get_profile_by_id(user_id)
    return schemas.GetUserProfileResponse.model_validate(profile.model_dump())


@router.get("/by_auth_user_id/{auth_user_id}", response_model=schemas.GetUserProfileResponse)
async def get_user_profile_by_auth_user_id(
        auth_user_id: int,
        service: IUserProfileService = Depends(get_user_profile_service)
):
    profile = await service.get_profile_by_auth_user_id(auth_user_id)
    return schemas.GetUserProfileResponse.model_validate(profile.model_dump())


@router.post("/by_auth_user_id", response_model=list[schemas.GetUserProfileResponse])
async def get_user_profiles_by_auth_user_ids(
        data: schemas.UserProfilesRequest,
        service: IUserProfileService = Depends(get_user_profile_service)
):
    """
    Метод обработки запроса на получение списка профилей пользователей
    по внешним id пользователей из сервиса авторизации.

    Примечание: Из-за необходимости передачи списка всех id
    используется POST запрос вместо GET как BULT GET запрос.
    """
    profiles = await service.get_profiles_by_auth_user_ids(data.ids)
    return [
        schemas.GetUserProfileResponse.model_validate(profile.model_dump())
        for profile in profiles
    ]


@router.post("/", response_model=schemas.CreateUserProfileResponse)
async def create_profile(
        data: schemas.CreateUserProfileRequest,
        user_profile_service: IUserProfileService = Depends(get_user_profile_service),
):
    dto_data = dto.CreateUserProfileCommand(**data.model_dump())
    dto_response = await user_profile_service.create_profile(dto_data)
    return schemas.CreateUserProfileResponse.model_validate(dto_response.model_dump())


@router.patch("/{user_id}", response_model=schemas.UpdateUserProfileResponse)
async def update_user_profile(
        user_id: int,
        data: schemas.UpdateUserProfileRequest,
        access_token: Annotated[str, Depends(oauth2_scheme)],
        user_profile_service: IUserProfileService = Depends(get_user_profile_service),
        token_service: ITokenService = Depends(get_token_service),
):
    token = await token_service.validate_token(access_token)
    if token is None:
        raise HTTPException(status_code=403, detail="Invalid token")
    dto_data = dto.UpdateUserProfileCommand(**data.model_dump())
    dto_response = await user_profile_service.update_profile(user_id, dto_data)
    return schemas.UpdateUserProfileResponse.model_validate(dto_response.model_dump())

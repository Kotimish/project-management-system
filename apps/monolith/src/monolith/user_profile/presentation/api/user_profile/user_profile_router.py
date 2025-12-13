from fastapi import APIRouter

from monolith.user_profile.presentation.schemas import user_profile as schemas

router = APIRouter(
    prefix="/user_profile",
    tags=["user profile"]
)


@router.get("/{user_id}", response_model=schemas.GetUserProfileResponse)
def get_user_profile(
        user_id: int
):
    raise NotImplementedError


@router.post("/", response_model=schemas.CreateUserProfileResponse)
def create_profile(
        data: schemas.CreateUserProfileRequest
):
    raise NotImplementedError


@router.post("/{user_id}", response_model=schemas.UpdateUserProfileResponse)
def update_user_profile(
        user_id: int,
        data: schemas.UpdateUserProfileRequest
):
    raise NotImplementedError

from fastapi import APIRouter

from monolith.user_profile.presentation.api.user_profile import user_profile_router

router = APIRouter(
    prefix='/api',
    tags=['api'],
)

router.include_router(user_profile_router)

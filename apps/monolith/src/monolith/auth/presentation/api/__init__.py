from fastapi import APIRouter

from monolith.auth.presentation.api.auth.auth_router import router as auth_router

router = APIRouter(
    prefix='/api',
    tags=['api'],
)

router.include_router(auth_router)

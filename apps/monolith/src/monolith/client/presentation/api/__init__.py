from fastapi import APIRouter

from monolith.client.presentation.api.client.client_router import router as client_router
from monolith.client.presentation.api.auth.auth_routes import router as auth_routes
from monolith.client.presentation.api.profile.profile_router import router as profile_router

router = APIRouter()

router.include_router(client_router)
router.include_router(auth_routes)
router.include_router(profile_router)

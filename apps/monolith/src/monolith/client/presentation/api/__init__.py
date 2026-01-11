from fastapi import APIRouter

from monolith.client.presentation.api.auth.auth_routes import router as auth_routes
from monolith.client.presentation.api.client.client_router import router as client_router
from monolith.client.presentation.api.profile.profile_router import router as profile_router
from monolith.client.presentation.api.project.project_router import router as project_router
from monolith.client.presentation.api.project.sprint_router import router as sprint_router
from monolith.client.presentation.api.project.task_router import router as task_router
from monolith.client.presentation.api.project.user_task_router import router as user_task_router
from monolith.client.presentation.api.project.participant_router import router as participant_router

router = APIRouter()

router.include_router(client_router)
router.include_router(auth_routes)
router.include_router(profile_router)
router.include_router(project_router)
router.include_router(sprint_router)
router.include_router(task_router)
router.include_router(user_task_router)
router.include_router(participant_router)

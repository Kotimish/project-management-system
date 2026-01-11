from fastapi import APIRouter

from monolith.project.presentation.api.participant import participant_router
from monolith.project.presentation.api.project import project_router
from monolith.project.presentation.api.sprint import sprint_router
from monolith.project.presentation.api.task import task_router
from monolith.project.presentation.api.task import user_task_router
from monolith.project.presentation.api.task_status import task_status_router

router = APIRouter(
    prefix='/api',
    tags=['api'],
)

router.include_router(participant_router)
router.include_router(project_router)
router.include_router(sprint_router)
router.include_router(task_router)
router.include_router(user_task_router)
router.include_router(task_status_router)

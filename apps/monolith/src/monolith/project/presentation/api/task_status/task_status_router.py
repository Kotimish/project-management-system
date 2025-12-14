from fastapi import APIRouter

router = APIRouter(
    prefix="/task_status",
    tags=["task_status"]
)


@router.get("/")
async def get_task_statuses():
    pass


@router.get("/{task_status_id}")
async def get_task_status():
    pass

from fastapi import APIRouter

router = APIRouter(
    prefix="/task",
    tags=["task"]
)


@router.get("/")
async def get_tasks():
    pass


@router.post("/")
async def create_task():
    pass


@router.get("/{task_id}")
async def get_task():
    pass


@router.put("/{task_id}")
async def update_task():
    pass


@router.delete("/{task_id}")
async def delete_task():
    pass

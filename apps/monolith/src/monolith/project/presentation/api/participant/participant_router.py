from fastapi import APIRouter

router = APIRouter(
    tags=["participant"]
)


@router.get("/projects/{project_id}/participants")
async def get_participants():
    pass


@router.post("/projects/{project_id}/participants")
async def add_participant():
    pass


@router.delete("/projects/{project_id}/participants/{user_id}")
async def delete_participant():
    pass

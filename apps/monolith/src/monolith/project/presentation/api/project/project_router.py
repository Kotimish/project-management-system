from fastapi import APIRouter

router = APIRouter(
    prefix="/project",
    tags=["project"]
)


@router.get("/")
async def get_projects():
    pass


@router.post("/")
async def create_project():
    pass


@router.get("/{project_id}")
async def get_project():
    pass


@router.put("/{project_id}")
async def update_project():
    pass


@router.delete("/{project_id}")
async def delete_project():
    pass

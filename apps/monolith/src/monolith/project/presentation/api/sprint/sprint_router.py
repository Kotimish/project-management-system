from fastapi import APIRouter

router = APIRouter(
    prefix="/sprint",
    tags=["sprint"]
)


@router.get("/")
async def get_sprints():
    pass


@router.post("/")
async def create_sprint():
    pass


@router.get("/{sprint_id}")
async def get_sprint():
    pass


@router.put("/{sprint_id}")
async def update_sprint():
    pass


@router.delete("/{sprint_id}")
async def delete_sprint():
    pass

from pydantic import BaseModel


class TaskStatusResponse(BaseModel):
    name: str
    slug: str
    description: str
    status_id: int

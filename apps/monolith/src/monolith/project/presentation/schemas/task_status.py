from pydantic import BaseModel


class TaskStatusResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: str

from pydantic import BaseModel


class TaskStatusDTO(BaseModel):
    id: int
    name: str
    slug: str
    description: str

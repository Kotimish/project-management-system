from pydantic import BaseModel


class TaskStatusResponse(BaseModel):
    """Схема для статуса задачи"""
    id: int
    name: str
    slug: str
    description: str

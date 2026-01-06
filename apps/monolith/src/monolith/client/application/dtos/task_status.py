from pydantic import BaseModel


class TaskStatusDTO(BaseModel):
    """DTO для модели статус задачи спринта проекта"""
    id: int
    name: str
    slug: str
    description: str

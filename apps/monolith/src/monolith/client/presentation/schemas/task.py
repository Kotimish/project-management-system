from pydantic import BaseModel


class CreateTaskSchema(BaseModel):
    """Схема для запроса создания задачи"""
    title: str
    description: str = None


class UpdateTaskSchema(BaseModel):
    """Схема для запроса создания задачи"""
    title: str | None = None
    description: str | None = None

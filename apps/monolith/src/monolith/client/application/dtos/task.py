from pydantic import BaseModel


class TaskDTO(BaseModel):
    """DTO для модели задача спринта проекта"""
    id: int
    title: str
    description: str
    project_id: int
    status_id: int
    assignee_id: int | None = None
    sprint_id: int | None = None


class CreateTaskCommand(BaseModel):
    """DTO для создания модели задача спринта проекта"""
    title: str
    assignee_id: int | None = None,
    description: str | None = None


class UpdateTaskCommand(BaseModel):
    """DTO для обновления модели задача спринта проекта"""
    title: str | None = None
    description: str | None = None
    status_id: int | None = None
    assignee_id: int | None = None
    sprint_id: int | None = None

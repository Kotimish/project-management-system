from pydantic import BaseModel


class UpdateTaskCommand(BaseModel):
    """Данные для запроса обновления задачи"""
    title: str | None = None
    description: str | None = None
    status_id: int | None = None
    assignee_id: int | None = None
    sprint_id: int | None = None


class TaskResponse(BaseModel):
    """Данные для ответа на запрос о получение информации о задаче"""
    id: int
    project_id: int
    status_id: int
    assignee_id: int | None
    sprint_id: int | None = None
    title: str | None
    description: str | None

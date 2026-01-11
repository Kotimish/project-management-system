from pydantic import BaseModel


class CreateTaskRequest(BaseModel):
    title: str
    assignee_id: int | None = None,
    description: str | None = None


class UpdateTaskRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    status_id: int | None = None
    assignee_id: int | None = None
    sprint_id: int | None = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    project_id: int
    status_id: int
    assignee_id: int | None = None
    sprint_id: int | None = None

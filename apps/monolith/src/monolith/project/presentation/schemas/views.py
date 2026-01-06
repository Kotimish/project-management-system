from datetime import date, datetime

from pydantic import BaseModel


# --- Упрощенные Схемы для Схем агрегатов ---

class TaskStatusDetail(BaseModel):
    """Данные о статусе задачи"""
    id: int
    name: str
    slug: str
    description: str | None


class TaskStatusReference(BaseModel):
    """Упрощенные данные о статусе задачи"""
    id: int
    name: str
    slug: str


class TaskDetail(BaseModel):
    """Данные о задаче"""
    id: int
    assignee_id: int | None
    title: str | None
    description: str | None
    status: TaskStatusReference
    created_at: datetime
    updated_at: datetime


class TaskWithStatusDetail(BaseModel):
    """Упрощенные данные о задаче со связанным статусом"""
    id: int
    title: str | None
    status: TaskStatusReference


class TaskReference(BaseModel):
    """Упрощенные данные о задаче"""
    id: int
    title: str | None


class SprintDetail(BaseModel):
    """Данные о спринте"""
    id: int
    name: str | None
    start_date: date
    end_date: date
    created_at: datetime
    updated_at: datetime


class SprintWithTaskDetail(BaseModel):
    """Данные о спринте со связанными задачами"""
    id: int
    name: str | None
    start_date: date
    end_date: date
    total_tasks: int
    completed_tasks: int
    created_at: datetime
    updated_at: datetime


class SprintReference(BaseModel):
    """Упрощенные данные о спринте"""
    id: int
    name: str | None


class ProjectDetail(BaseModel):
    """Данные о проекте"""
    id: int
    owner_id: int
    name: str | None
    description: str | None
    created_at: datetime
    updated_at: datetime


class ProjectReference(BaseModel):
    """Упрощенные данные о проекте"""
    id: int
    name: str | None


# --- Схемы Агрегаты ---

class ProjectView(BaseModel):
    """Агрегат данные для отображения информации о проекте"""
    project: ProjectDetail
    sprints: list[SprintWithTaskDetail]


class SprintView(BaseModel):
    """Агрегат данные для отображения информации о спринте"""
    project: ProjectReference
    sprint: SprintWithTaskDetail
    tasks: list[TaskWithStatusDetail]


class TaskView(BaseModel):
    """Агрегат данные для отображения информации о задаче"""
    project: ProjectReference
    sprint: SprintReference
    task: TaskDetail

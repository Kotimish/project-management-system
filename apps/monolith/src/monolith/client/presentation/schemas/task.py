from pydantic import BaseModel, field_validator


class CreateTaskSchema(BaseModel):
    """Схема для запроса создания задачи"""
    title: str
    assignee: str | None = None
    description: str = None

    @field_validator('assignee', mode='before')
    @classmethod
    def empty_string_to_none(cls, value):
        if value == "" or value == "None":
            return None
        return value


class UpdateTaskSchema(BaseModel):
    """Схема для запроса изменения задачи"""
    title: str | None = None
    status: int | None = None
    assignee: str | None = None
    description: str | None = None

    @field_validator('assignee', mode='before')
    @classmethod
    def empty_string_to_none(cls, value):
        if value == "" or value == "None":
            return None
        return value

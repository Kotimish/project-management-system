from pydantic import BaseModel


class Breadcrumb(BaseModel):
    """Схема для навигационной цепочки"""
    name: str
    url: str
    is_active: bool

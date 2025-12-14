from pydantic import BaseModel
from pydantic import HttpUrl
from pydantic import Field

class URLConfig(BaseModel):
    """Настройки различных путей к сервисам"""
    auth_service: HttpUrl = Field(default="http://127.0.0.1:8000/")
    user_profile_service: HttpUrl = Field(default="http://127.0.0.1:8000/")

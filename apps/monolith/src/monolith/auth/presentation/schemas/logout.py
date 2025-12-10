from pydantic import BaseModel


class LogoutResponseScheme(BaseModel):
    msg: str

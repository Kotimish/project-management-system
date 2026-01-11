from pydantic import BaseModel, SecretStr


class LoginRequest(BaseModel):
    login: str
    password: SecretStr


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str

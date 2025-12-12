from pydantic import BaseModel, SecretStr


class CreateUserCommand(BaseModel):
    login: str
    email: str
    password: SecretStr


class CreateUserResponse(BaseModel):
    id: int


class LoginUserCommand(BaseModel):
    login: str
    password: SecretStr


class LoginUserResponse(BaseModel):
    access_token: str
    refresh_token: str

from monolith.auth.application.dtos.user import CreateUserCommand
from monolith.auth.application.interfaces.factories.user_factory import IUserFactory
from monolith.auth.domain.model.user import User


class UserFactory(IUserFactory):
    """Фабрика модели Пользователь"""
    def create(self, data: CreateUserCommand, hashed_password: str, role_id: int) -> User:
        return User(
            login=data.login,
            email=data.email,
            hashed_password=hashed_password,
            role_id=role_id
        )

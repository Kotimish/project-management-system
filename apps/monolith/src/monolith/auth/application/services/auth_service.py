from datetime import datetime, timezone

from monolith.auth.application.dtos.token import RefreshTokenDTO
from monolith.auth.application.dtos.user import LoginUserCommand, LoginUserResponse
from monolith.auth.application.exceptions import auth_exceptions as exceptions
from monolith.auth.application.interfaces.security.hash_service import IHashService
from monolith.auth.application.interfaces.services.auth_service import IAuthenticationService
from monolith.auth.application.interfaces.services.role_service import IRoleService
from monolith.auth.application.interfaces.services.session_service import ISessionService
from monolith.auth.application.interfaces.services.token_service import ITokenService
from monolith.auth.application.interfaces.services.user_service import IUserService


class AuthenticationService(IAuthenticationService):
    """Сервис авторизации и аутентификации пользователей"""

    def __init__(
            self,
            user_service: IUserService,
            role_service: IRoleService,
            session_service: ISessionService,
            token_service: ITokenService,
            hash_service: IHashService
    ):
        self.user_service = user_service
        self.role_service = role_service
        self.session_service = session_service
        self.token_service = token_service
        self.hash_service = hash_service

    async def login_user(self, data: LoginUserCommand) -> LoginUserResponse:
        # Получение и проверки пользователя
        user = await self.user_service.get_user_by_login(data.login)
        if not user:
            raise exceptions.InvalidLoginException("Login not found")
        if not self.hash_service.verify(data.password.get_secret_value(), user.hashed_password):
            raise exceptions.InvalidPasswordException("Password is incorrect")
        if not user.is_active:
            raise exceptions.InactiveUserException("Inactive user")
        # Получение роли для генерации токенов
        role = await self.role_service.get_role_by_id(user.role_id)
        # Создание сессии
        session = await self.session_service.create_session(user)
        # Генерация токенов
        access_token = self.token_service.create_access_token(user, role)
        refresh_token = self.token_service.create_refresh_token(user, role, session)
        return LoginUserResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )

    async def logout_user(self, refresh_token: str) -> bool:
        pyload = self.token_service.decode_token(refresh_token)
        data = RefreshTokenDTO(**pyload)
        return await self.session_service.revoke_session(data.session_id)

    async def refresh_access_token(self, refresh_token: str) -> str:
        pyload = self.token_service.decode_token(refresh_token)
        data = RefreshTokenDTO(**pyload)
        # Проверка на существование сессии по этому токену
        session = await self.session_service.get_session_by_id(data.session_id)
        if not session:
            raise exceptions.InvalidSessionException("Session not found")
        if not session.is_active:
            raise exceptions.InactiveSessionException("Inactive session")
        # Получение и проверки пользователя
        user = await self.user_service.get_user_by_id(data.sub)
        if not user:
            raise exceptions.NotFoundUserException("User not found")
        if not user.is_active:
            raise exceptions.InactiveUserException("Inactive user")
        # Получение роли для генерации токенов
        role = await self.role_service.get_role_by_id(user.role_id)
        return self.token_service.create_access_token(user, role)

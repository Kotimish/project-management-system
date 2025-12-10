from fastapi import Request

from monolith.auth.application.interfaces.security.hash_service import IHashService
from monolith.auth.application.interfaces.security.jwt_service import IJWTService
from monolith.auth.application.interfaces.services.auth_service import IAuthenticationService
from monolith.auth.application.interfaces.services.role_service import IRoleService
from monolith.auth.application.interfaces.services.session_service import ISessionService
from monolith.auth.application.interfaces.services.token_service import ITokenService
from monolith.auth.application.interfaces.services.user_service import IUserService
from monolith.auth.application.services.auth_service import AuthenticationService
from monolith.auth.application.services.role_service import RoleService
from monolith.auth.application.services.session_service import SessionService
from monolith.auth.application.services.token_service import TokenService
from monolith.auth.application.services.user_service import UserService
from monolith.auth.infrastructure.factories.session_factory import SessionFactory
from monolith.auth.infrastructure.factories.user_factory import UserFactory
from monolith.auth.infrastructure.security.bcrypt_hash_service import BcryptHashService
from monolith.auth.infrastructure.security.key_loader import load_key
from monolith.auth.infrastructure.security.py_jwt_service import PyJWTService
from monolith.config.settings import settings


def get_auth_service(request: Request) -> IAuthenticationService:
    user_service = get_user_service(request)
    role_service = get_role_service(request)
    session_service = get_session_service(request)
    token_service = get_token_service()
    hash_service = get_hash_service()
    return AuthenticationService(
        user_service,
        role_service,
        session_service,
        token_service,
        hash_service
    )


def get_user_service(request: Request) -> IUserService:
    factory = UserFactory()
    repository = request.app.state.user_repository
    role_service = get_role_service(request)
    hash_service = get_hash_service()
    return UserService(factory, repository, role_service, hash_service)


def get_role_service(request: Request) -> IRoleService:
    repository = request.app.state.role_repository
    return RoleService(repository)


def get_session_service(request: Request) -> ISessionService:
    factory = SessionFactory()
    repository = request.app.state.session_repository
    return SessionService(factory, repository,  settings.auth)


def get_token_service() -> ITokenService:
    jwt_service = get_jwt_service()
    return TokenService(jwt_service, settings.auth)


def get_jwt_service() -> IJWTService:
    private_key = load_key(settings.auth.private_key_path)
    public_key = load_key(settings.auth.public_key_path)
    algorithm = settings.auth.algorithm
    return PyJWTService(private_key, public_key, algorithm)


def get_hash_service() -> IHashService:
    return BcryptHashService()

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import AsyncGenerator

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
from monolith.auth.domain.interfaces.repositories.role_repository import IRoleRepository
from monolith.auth.domain.interfaces.repositories.session_repository import ISessionRepository
from monolith.auth.domain.interfaces.repositories.user_repository import IUserRepository
from monolith.auth.infrastructure.factories.session_factory import SessionFactory
from monolith.auth.infrastructure.factories.user_factory import UserFactory
from monolith.auth.infrastructure.repositories.role import ORMRoleRepository
from monolith.auth.infrastructure.repositories.session import ORMSessionRepository
from monolith.auth.infrastructure.repositories.user import ORMUserRepository
from monolith.auth.infrastructure.security.bcrypt_hash_service import BcryptHashService
from monolith.auth.infrastructure.security.key_loader import load_key
from monolith.auth.infrastructure.security.py_jwt_service import PyJWTService
from monolith.config.settings import settings
from monolith.infrastructure.database import async_session


async def get_async_session() -> AsyncGenerator[AsyncSession]:
    async with async_session() as session:
        yield session


async def get_role_repository(
        session: AsyncSession = Depends(get_async_session)
) -> IRoleRepository:
    return ORMRoleRepository(session)


async def get_users_repository(
        session: AsyncSession = Depends(get_async_session)
) -> IUserRepository:
    return ORMUserRepository(session)


async def get_session_repository(
        session: AsyncSession = Depends(get_async_session)
) -> ISessionRepository:
    return ORMSessionRepository(session)


def get_role_service(
        repository=Depends(get_role_repository)
) -> IRoleService:
    return RoleService(repository)


def get_user_service(
        repository=Depends(get_users_repository),
        role_service=Depends(get_role_service),
) -> IUserService:
    factory = UserFactory()
    hash_service = get_hash_service()
    return UserService(factory, repository, role_service, hash_service)


def get_session_service(
        repository=Depends(get_session_repository)
) -> ISessionService:
    factory = SessionFactory()
    return SessionService(factory, repository, settings.auth)


def get_auth_service(
        user_service=Depends(get_user_service),
        role_service=Depends(get_role_service),
        session_service=Depends(get_session_service),
) -> IAuthenticationService:
    token_service = get_token_service()
    hash_service = get_hash_service()
    return AuthenticationService(
        user_service,
        role_service,
        session_service,
        token_service,
        hash_service
    )


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

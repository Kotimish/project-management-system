from datetime import datetime, timezone, timedelta

from monolith.auth.application.interfaces.security.jwt_service import IJWTService
from monolith.auth.application.interfaces.services.token_service import ITokenService
from monolith.auth.domain.model import Role, Session, User
from monolith.config.auth_config import AuthConfig


class TokenService(ITokenService):
    """Сервис работы с токенами пользователей"""

    def __init__(self, jwt_service: IJWTService, config: AuthConfig):
        self.jwt_service = jwt_service
        self.config = config

    def create_access_token(self, user: User, role: Role) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.config.access_token_expire_minutes)
        data = {
            "sub": str(user.id),
            "role_slug": role.slug,
            "exp": str(int(expire.timestamp()))
        }
        return self.jwt_service.encode(data)

    def create_refresh_token(self, user: User, role: Role, session: Session) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.config.refresh_token_expire_minutes)
        data = {
            "sub": str(user.id),
            "role_slug": role.slug,
            "session_id": str(session.id),
            "exp": str(int(expire.timestamp()))
        }
        return self.jwt_service.encode(data)

    def decode_token(self, token: str) -> dict:
        return self.jwt_service.decode(token)


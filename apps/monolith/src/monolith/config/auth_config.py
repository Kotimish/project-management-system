from pathlib import Path

from pydantic import BaseModel


class AuthConfig(BaseModel):
    """Настройки для JWT (путь к приватному ключу и алгоритм)."""
    private_key_path: Path
    public_key_path: Path
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_minutes: int = 60

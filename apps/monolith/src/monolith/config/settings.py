from enum import Enum
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from monolith.config.auth_config import AuthConfig
from monolith.config.db_config import DbConfig

# monolith/src/monolith/config/settings.py
# monolith/ — корень проекта, содержит .env и .env.default
BASE_DIR = Path(__file__).resolve().parents[3]

class Environment(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="MONOLITH__",
        env_nested_delimiter="__",
        env_file=(
            BASE_DIR / ".env.default",
            BASE_DIR / ".env",
        ),
    )
    env: Environment = Environment.DEVELOPMENT
    auth: AuthConfig
    db: DbConfig


settings = Settings()
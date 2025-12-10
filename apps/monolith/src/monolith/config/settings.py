from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

from monolith.config.auth_config import AuthConfig

# monolith/src/monolith/config/settings.py
# monolith/ — корень проекта, содержит .env и .env.default
BASE_DIR = Path(__file__).resolve().parents[3]

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="MONOLITH__",
        env_nested_delimiter="__",
        env_file=(
            BASE_DIR / ".env.default",
            BASE_DIR / ".env",
        ),
    )

    auth: AuthConfig


settings = Settings()
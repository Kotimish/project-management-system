from pydantic import BaseModel, SecretStr
from sqlalchemy import URL


class DbConfig(BaseModel):
    driver_sync: str = "postgresql+psycopg"
    driver_async: str = "postgresql+asyncpg"

    echo: bool = False
    host: str
    port: int = 5432
    database: str

    username: str
    password: SecretStr

    max_overflow: int = 0
    pool_size: int = 50

    def build_url(self, driver_name: str) -> URL:
        return URL.create(
            driver_name,
            host=self.host,
            port=self.port,
            database=self.database,
            username=self.username,
            password=self.password.get_secret_value(),
        )

    @property
    def url(self) -> URL:
        return self.build_url(self.driver_sync)

    @property
    def async_url(self) -> URL:
        return self.build_url(self.driver_async)

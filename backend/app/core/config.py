from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "PAREEK AI RED TEAM"
    environment: str = "development"

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "pareek"

    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0

    secret_key: str = "change-me"
    jwt_algorithm: str = "HS256"

    allowed_scan_modes: list[str] = [
        "PASSIVE",
        "SAFE",
        "STANDARD",
        "DEEP",
        "API",
        "AUTHENTICATED",
        "FULL_ASSESSMENT",
    ]

    max_request_budget: int = 2500
    max_concurrency: int = 4
    default_scan_mode: str = "SAFE"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def postgres_dsn(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@"
            f"{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def redis_dsn(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"


@lru_cache
def get_settings() -> Settings:
    return Settings()

from typing import Literal

from pydantic import field_validator
from pydantic_settings import BaseSettings as PydanticBaseSettings
from pydantic_settings import SettingsConfigDict

AppEnv = Literal["development", "production", "test"]


class AppSettings(PydanticBaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    APP_ENV: AppEnv = "development"
    APP_VERSION: str = "0.1.0"

    SERVER_HOST: str = "0.0.0.0"  # nosec B104
    SERVER_PORT: int = 8000

    JWT_SECRET: str = "change-me-super-secret"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    POSTGRES_HOST: str = "127.0.0.1"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "fastapi_core_clean"
    POSTGRES_PORT: int = 5432

    POSTGRES_HOST_TEST: str = "127.0.0.1"
    POSTGRES_USER_TEST: str = "postgres"
    POSTGRES_PASSWORD_TEST: str = "postgres"
    POSTGRES_DB_TEST: str = "fastapi_core_clean_test"
    POSTGRES_PORT_TEST: int = 5432

    CORS_ORIGINS: str = (
        "http://localhost:5173,http://127.0.0.1:5173,"
        "http://localhost:3000,http://127.0.0.1:3000"
    )

    THROTTLE_TTL_SECONDS: int = 60
    THROTTLE_LIMIT: int = 10

    SWAGGER_DOCS_PATH: str = "/api_docs"
    SWAGGER_OPENAPI_PATH: str = "/openapi.json"
    SWAGGER_REDOC_PATH: str = "/redoc"

    SEED_ON_BOOT: bool = True

    SUPER_USER_NAME: str = "admin"
    SUPER_USER_USERNAME: str = "admin"
    SUPER_USER_PASSWORD: str = "admin"

    MEMBER_USER_NAME: str | None = "member"
    MEMBER_USER_USERNAME: str | None = "member"
    MEMBER_USER_PASSWORD: str | None = "member"

    @field_validator("APP_ENV", mode="before")
    @classmethod
    def normalize_app_env(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip().lower()
        return value

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"

    @property
    def is_test(self) -> bool:
        return self.APP_ENV == "test"

    @property
    def docs_enabled(self) -> bool:
        return not self.is_production

    @property
    def cors_origin_list(self) -> list[str]:
        raw = self.CORS_ORIGINS.strip()
        if raw == "*":
            return ["*"]
        return [origin.strip() for origin in raw.split(",") if origin.strip()]

    @property
    def auth_rate_limit(self) -> str:
        return f"{self.THROTTLE_LIMIT}/{self.THROTTLE_TTL_SECONDS}seconds"

    @property
    def database_url_asy(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def database_test_asy(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER_TEST}:"
            f"{self.POSTGRES_PASSWORD_TEST}@{self.POSTGRES_HOST_TEST}:"
            f"{self.POSTGRES_PORT_TEST}/{self.POSTGRES_DB_TEST}"
        )

    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


settings = AppSettings()  # type: ignore[call-arg]

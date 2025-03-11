from dataclasses import field
from typing import Optional

from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, PostgresDsn, field_validator


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    auth: str = "/auth"
    users: str = "/users"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()

    @property
    def bearer_token_url(self) -> str:
        parts = (self.prefix, self.v1.prefix, self.v1.auth, "/login")
        path = "".join(parts)
        return path.removeprefix("/")


class DatabaseConfig(BaseModel):
    host: Optional[str] = None
    port: Optional[int] = None
    user: Optional[str] = None
    password: Optional[str] = None
    name: Optional[str] = None
    url: Optional[PostgresDsn] = None
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = field(default_factory=lambda: {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    })

    @field_validator('url', mode='before')
    @classmethod
    def validate_url(cls, value: Optional[PostgresDsn], values: ValidationInfo) -> Optional[PostgresDsn]:
        if value:
            return value

        required_fields = ["host", "port", "user", "password", "name"]
        if not all(values.data.get(required_field) for required_field in required_fields):
            raise ValueError(
                "If 'url' is not set, you need to specify 'host', 'port', 'user', 'password' and 'name'.")

        return PostgresDsn.build(
            scheme="postgresql",
            username=values.data['user'],
            password=values.data['password'],
            host=values.data['host'],
            port=values.data['port'],
            path=f"/{values.data['name']}",
        )


class AccessToken(BaseModel):
    lifetime_seconds: int = 3600
    reset_password_token_secret: Optional[str] = None
    verification_token_secret: Optional[str] = None


class Settings(BaseSettings):
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig = DatabaseConfig()
    access_token: AccessToken = AccessToken()

    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        env_prefix="APP_CONFIG__",
        env_nested_delimiter="__",
    )


settings = Settings()

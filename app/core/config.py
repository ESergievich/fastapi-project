from typing import Any, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, PostgresDsn, field_validator


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


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

    @field_validator('url', mode='before')
    @classmethod
    def validate_url(cls, value: Optional[str], values: dict[str, Any]) -> Optional[PostgresDsn]:
        if value:
            return value

        required_fields = ["host", "port", "user", "password", "name"]
        if not all(values.get(field) for field in required_fields):
            raise ValueError(
                "If 'url' is not set, you need to specify 'host', 'port', 'user', 'password' and 'name'.")

        return PostgresDsn.build(
            scheme="postgresql",
            username=values['user'],
            password=values['password'],
            host=values['host'],
            port=values['port'],
            path=f"/{values['name']}",
        )


class Settings(BaseSettings):
    run: RunConfig = RunConfig()
    db: DatabaseConfig = DatabaseConfig()

    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        env_prefix="APP_CONFIG__",
        env_nested_delimiter="__",
    )


settings = Settings()

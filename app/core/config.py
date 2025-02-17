from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class Settings(BaseSettings):
    run: RunConfig = RunConfig()

    model_config = SettingsConfigDict(
        env_file=("example.env", ".env"),
        env_prefix="APP_CONFIG__",
        env_nested_delimiter="__",
    )


settings = Settings()

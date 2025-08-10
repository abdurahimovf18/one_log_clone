from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from .enums import LogLevel

ROOT = Path(__file__).resolve().parent.parent.parent


class Env(BaseSettings):
    DEBUG: bool
    LOG_LEVEL: LogLevel

    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str | None = None
    REDIS_DB: int

    model_config = SettingsConfigDict(
        env_file=ROOT / ".env",
    )

    
env = Env()  # type: ignore

# sqlalchemy url: database+driver://{user}:{password}@{host}:{port}/{db_name} 
DATABASE_URL = (
    f"postgresql+psycopg://{env.DATABASE_USER}:{env.DATABASE_PASSWORD}"
    f"@{env.DATABASE_HOST}:{env.DATABASE_PORT}/{env.DATABASE_NAME}"
)

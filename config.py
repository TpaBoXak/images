from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic import RedisDsn

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict
from pathlib import Path

class RunConfig(BaseModel):
    host: str
    port: int


class ApiPrefix (BaseModel):
    prefix: str = "/api"
    auth_prefix: str = "/auth"
    images_prefix: str = "/images"

class DatabaseConfig(BaseModel): 
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

class ImagesFolder(BaseModel):
    path: Path = Path("./app/static")

class JWTConfig(BaseModel):
    token_hours: int = 12


class RedisConfig(BaseModel):
    url: RedisDsn

class RabbitMQConfig(BaseModel):
    url: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", ".env.template"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONF__"
    )
    run: RunConfig
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig
    jwt: JWTConfig = JWTConfig()
    redis: RedisConfig
    images_folder: ImagesFolder = ImagesFolder()
    ALLOWED_EXTENSIONS: set[str] = {"png", "jpg", "jpeg"}
    rabbitmq: RabbitMQConfig    


settings: Settings = Settings()
print(settings.redis.url, settings.rabbitmq.url, settings.run.port, settings.run.host)
from pydantic import field_validator, PostgresDsn
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings


class JwtConfig(BaseSettings):
    secret_key: str = "d2a73573-da3a-44d2-bb4e-5a9dceae01a2"
    refresh_secret_key: str = "68b94237-fd46-4ae7-b71f-afb7b6c5dd82"


class PostgresConfig(BaseSettings):
    scheme: str = "postgresql+asyncpg"
    host: str = "localhost"
    port: str = "5432"
    user: str = "postgres"
    password: str = "postgres"
    db: str = "standard"
    pool_size: int = 10
    pool_overflow_size: int = 10
    echo: bool = False
    dsn: str | None = None

    @field_validator('dsn')
    def assemble_db_connection(cls, v: str | None, values: ValidationInfo) -> str:
        values = values.data
        if isinstance(v, str):
            return v
        return str(
            PostgresDsn.build(
                scheme=values.get("scheme"),
                username=values.get("user"),
                password=values.get("password"),
                host=values.get("host"),
                port=int(values.get("port")),
                path=f"{values.get('db')}",
            )
        )


class Settings(BaseSettings):
    jwt: JwtConfig = JwtConfig(_env_prefix="jwt_")
    database: PostgresConfig = PostgresConfig(_env_prefix="postgres_")

    class Config:
        env_file = ".env"
import os

from pydantic import field_validator, PostgresDsn
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings

project_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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


class TelegramSettings(BaseSettings):
    token: str = ""


class ClassifierModelSettings(BaseSettings):
    path: str = os.path.join(project_dir, 'models/text_classifier.joblib')


class NERModelSettings(BaseSettings):
    path: str = os.path.join(project_dir, 'models/ner_model')


class Settings(BaseSettings):
    jwt: JwtConfig = JwtConfig(_env_prefix="jwt_")
    database: PostgresConfig = PostgresConfig(_env_prefix="postgres_")
    telegram: TelegramSettings = TelegramSettings(_env_prefix="telegram_")
    classifier_model: ClassifierModelSettings = ClassifierModelSettings(_env_prefix="classifier_model_")
    ner_model: NERModelSettings = NERModelSettings(_env_prefix="ner_model_")

    class Config:
        env_file = ".env"

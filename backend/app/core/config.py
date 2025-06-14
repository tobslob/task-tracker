import os
from typing import List

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

ENV: str = ""


class Configs(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True)
    # base
    ENV: str = os.getenv("ENV", "dev")
    API: str = "/api"
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "fca-api"
    ENV_DATABASE_MAPPER: dict = {
        "prod": "fca",
        "stage": "stage-fca",
        "dev": "dev-fca",
        "test": "test-fca",
    }
    DB_ENGINE_MAPPER: dict = {
        "postgresql": "postgresql",
        "mysql": "mysql+pymysql",
        "sqlite": "sqlite",
    }

    PROJECT_ROOT: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # date
    DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S"
    DATE_FORMAT: str = "%Y-%m-%d"

    # auth
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 60 minutes * 24 hours * 30 days = 30 days

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = os.getenv(
        "BACKEND_CORS_ORIGINS", "http://localhost:3000"
    ).split(",")

    # database
    DB: str = os.getenv("DB", "sqlite")
    DB_USER: str = os.getenv("DB_USER", "")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_HOST: str = os.getenv("DB_HOST", "")
    DB_PORT: str = os.getenv("DB_PORT", "3306")
    DB_ENGINE: str = DB_ENGINE_MAPPER.get(DB, "postgresql")
    DB_MEMORY: bool = os.getenv("DB_MEMORY", "0").lower() in ["1", "true", "yes"]
    DATABASE_URL: str | None = os.getenv("DATABASE_URL")

    DATABASE_URI_FORMAT: str = "{db_engine}://{user}:{password}@{host}:{port}/{database}"

    if DATABASE_URL:
        DATABASE_URI: str = DATABASE_URL
    elif DB == "sqlite":
        if DB_MEMORY:
            DATABASE_URI: str = "sqlite:///:memory:"
        else:
            DATABASE_URI: str = f"sqlite:///./{ENV_DATABASE_MAPPER[ENV]}.db"
    else:
        DATABASE_URI: str = "{db_engine}://{user}:{password}@{host}:{port}/{database}".format(
            db_engine=DB_ENGINE,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=ENV_DATABASE_MAPPER[ENV],
        )

    # find query
    PAGE: int = 1
    PAGE_SIZE: int = 20
    ORDERING: str = "-id"


class TestConfigs(Configs):
    ENV: str = "test"


configs = Configs()

if ENV == "prod":
    pass
elif ENV == "stage":
    pass
elif ENV == "test":
    setting = TestConfigs()

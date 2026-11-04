from pathlib import Path

from pydantic import PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import TypedDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE_PATH = PROJECT_ROOT / ".env"


class ConnectionParams(TypedDict, closed=True):
    host: str
    port: int
    dbname: str
    user: str
    password: str


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str
    db_user: str
    db_pass: SecretStr

    @property
    def dsn(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql",
                username=self.db_user,
                password=self.db_pass.get_secret_value(),
                host=self.db_host,
                port=self.db_port,
                path=self.db_name,
            )
        )

    @property
    def connection_params(self) -> ConnectionParams:
        return {
            "host": self.db_host,
            "port": self.db_port,
            "dbname": self.db_name,
            "user": self.db_user,
            "password": self.db_pass.get_secret_value(),
        }


settings = DatabaseSettings()

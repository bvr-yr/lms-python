"""Pydantic-based configuration management and environment parsing."""

from pathlib import Path
from typing import Literal

from pydantic import PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import TypedDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE_PATH = PROJECT_ROOT / ".env"

DEFAULT_LOG_LEVEL = "ERROR"

MODEL_CONFIG = SettingsConfigDict(
    env_file=ENV_FILE_PATH,
    env_file_encoding="utf-8",
    extra="ignore",
    case_sensitive=False,
)


class ConnectionParams(TypedDict, closed=True):
    """Type definition for PostgreSQL connection parameters."""

    host: str
    port: int
    dbname: str
    user: str
    password: str


class AppSettings(BaseSettings):
    """Application-level settings including logging configuration."""

    model_config = MODEL_CONFIG
    lms_log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = (
        DEFAULT_LOG_LEVEL
    )


class DatabaseSettings(BaseSettings):
    """Database credentials and connection configuration loaded from the environment."""

    model_config = MODEL_CONFIG

    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str
    db_user: str
    db_pass: SecretStr

    @property
    def dsn(self) -> str:
        """Build a standard PostgreSQL Data Source Name (DSN) URI.

        :return: Fully qualified database connection URI.
        :rtype: str
        """
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
        """Convert validated instance settings into psycopg connection parameters.

        :return: Parameter dictionary matching psycopg.connect kwargs.
        :rtype: ConnectionParams
        """
        return {
            "host": self.db_host,
            "port": self.db_port,
            "dbname": self.db_name,
            "user": self.db_user,
            "password": self.db_pass.get_secret_value(),
        }


app_settings = AppSettings()
db_settings = DatabaseSettings()

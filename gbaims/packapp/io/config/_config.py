from pydantic import BaseSettings

from ._environment import EnvironmentConfig


class Config(BaseSettings):
    environment: EnvironmentConfig

    class Config(BaseSettings.Config):
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"

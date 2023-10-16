from enum import Enum

from pydantic import BaseModel, BaseSettings

from gbaims.packapp.io.bergler import BerglerConfig
from gbaims.packapp.io.shopify import ShopifyConfig


class EnvironmentConfig(Enum):
    DEVELOPMENT = "DEVELOPMENT"
    PRODUCTION = "PRODUCTION"

    def is_development(self) -> bool:
        return self == EnvironmentConfig.DEVELOPMENT

    def is_production(self) -> bool:
        return self == EnvironmentConfig.PRODUCTION


class LoggingConfig(BaseModel):
    level: str

    def as_dict(self):
        return {
            "version": 1,
            "root": {"level": "ERROR", "handlers": ["stderr"]},
            "loggers": {
                # "gunicorn.access": {"level": self.level, "handlers": ["stdout"]},
                # "gunicorn.error": {"level": self.level, "handlers": ["stderr"]},
                # "werkzeug": {"level": self.level, "handlers": ["stderr"]},
            },
            "handlers": {
                "stdout": {
                    "class": "logging.StreamHandler",
                    "formatter": "simple",
                    "stream": "ext://sys.stdout",
                },
                "stderr": {
                    "class": "logging.StreamHandler",
                    "formatter": "simple",
                    "stream": "ext://sys.stderr",
                    "level": "DEBUG",
                },
            },
            "formatters": {
                "simple": {
                    "format": "%(levelname)-5s | %(message)s [%(name)s]",
                    "class": "logging.Formatter",
                }
            },
        }


class Config(BaseSettings):
    environment: EnvironmentConfig
    logging: LoggingConfig
    bergler: BerglerConfig
    shopify: ShopifyConfig

    class Config(BaseSettings.Config):
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"

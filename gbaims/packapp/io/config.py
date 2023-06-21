from enum import Enum

from pydantic import BaseSettings

from gbaims.packapp.io.shopify import ShopifyConfig


class EnvironmentConfig(Enum):
    DEVELOPMENT = "DEVELOPMENT"
    PRODUCTION = "PRODUCTION"

    def is_development(self) -> bool:
        return self == EnvironmentConfig.DEVELOPMENT

    def is_production(self) -> bool:
        return self == EnvironmentConfig.PRODUCTION


class Config(BaseSettings):
    environment: EnvironmentConfig
    shopify: ShopifyConfig

    class Config(BaseSettings.Config):
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"

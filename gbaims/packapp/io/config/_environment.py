from enum import Enum


class EnvironmentConfig(Enum):
    DEVELOPMENT = "DEVELOPMENT"
    PRODUCTION = "PRODUCTION"

    def is_development(self) -> bool:
        return self == EnvironmentConfig.DEVELOPMENT

    def is_production(self) -> bool:
        return self == EnvironmentConfig.PRODUCTION

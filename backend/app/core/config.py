from typing import Any, Union
import os
from pydantic import BaseModel, Field


def parse_cors_origins(v: Union[str, list[str], None]) -> list[str]:
    """Parse CORS origins from string or list"""
    if isinstance(v, str):
        return [origin.strip() for origin in v.split(",")]
    elif isinstance(v, list):
        return [str(origin) for origin in v]
    return []


class Settings(BaseModel):
    """
    Application settings for the in-memory database service.
    Environment variables take precedence over default values.
    """

    # API settings
    API_V1_STR: str = Field("/api/v1", description="API version 1 path prefix")

    # Environment settings
    ENVIRONMENT: str = Field(
        "development", description="Environment (development, testing, production)"
    )
    DEBUG: bool = Field(True, description="Debug mode flag")

    # CORS settings
    CORS_ORIGINS: list[str] = Field(
        default=["http://localhost", "http://localhost:8000", "http://localhost:3000"],
        description="List of allowed CORS origins",
    )

    # Service settings
    SERVICE_NAME: str = Field(
        "In-Memory Database Service", description="Name of the service"
    )
    SERVICE_VERSION: str = Field("1.0.0", description="Service version")
    SERVICE_DESCRIPTION: str = Field(
        "A FastAPI service providing in-memory database operations",
        description="Service description",
    )

    def configure_for_environment(self) -> None:
        """Apply environment-specific configurations"""
        if self.ENVIRONMENT == "production":
            self.DEBUG = False
            # In production, only accept specified origins
            if isinstance(self.CORS_ORIGINS, str) and self.CORS_ORIGINS == "*":
                raise ValueError(
                    "CORS_ORIGINS must be explicitly specified in production"
                )
        elif self.ENVIRONMENT == "testing":
            self.DEBUG = True
            self.CORS_ORIGINS = ["*"]  # Allow all origins in testing

    @classmethod
    def from_env(cls) -> "Settings":
        """Create settings from environment variables"""
        env_settings: dict[str, Any] = {}
        for field_name, field in cls.model_fields.items():
            env_value = os.getenv(field_name.upper())
            if env_value is not None:
                if field_name == "CORS_ORIGINS":
                    env_settings[field_name] = parse_cors_origins(env_value)
                elif field_name == "DEBUG":
                    env_settings[field_name] = env_value.lower() == "true"
                else:
                    env_settings[field_name] = env_value
        return cls(**env_settings)


# Create settings instance
settings = Settings.from_env()

# Apply environment-specific configurations
settings.configure_for_environment()

# Export settings instance
__all__ = ["settings"]

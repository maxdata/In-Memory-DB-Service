from typing import Any

from pydantic_settings import BaseSettings


def parse_cors_origins(v: Any) -> list[str]:
    """Parse CORS origins from string or list"""
    if isinstance(v, str):
        return [origin.strip() for origin in v.split(",")]
    elif isinstance(v, list):
        return [str(origin) for origin in v]
    return []


class Settings(BaseSettings):
    """
    Application settings for the in-memory database service.
    Environment variables take precedence over default values.
    """

    # API settings
    API_V1_STR: str = "/api/v1"

    # Environment settings
    ENVIRONMENT: str = "development"  # Options: development, testing, production
    DEBUG: bool = True

    # CORS settings
    CORS_ORIGINS: list[str] = [
        "http://localhost",
        "http://localhost:8000",
        "http://localhost:3000",
    ]

    # Service settings
    SERVICE_NAME: str = "In-Memory Database Service"
    SERVICE_VERSION: str = "1.0.0"
    SERVICE_DESCRIPTION: str = (
        "A FastAPI service providing in-memory database operations"
    )

    class Config:
        env_file = ".env"
        case_sensitive = True

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


# Create settings instance
settings = Settings()

# Apply environment-specific configurations
settings.configure_for_environment()

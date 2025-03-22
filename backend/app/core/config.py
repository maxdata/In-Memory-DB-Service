"""Configuration settings for the application."""

from pydantic import BaseModel


class Settings(BaseModel):
    """Application settings."""

    API_V1_STR: str = "/api/v1"
    API_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost", "http://localhost:8000"]
    SERVICE_NAME: str = "In-Memory Database Service"
    SERVICE_VERSION: str = "1.0.0"
    SERVICE_DESCRIPTION: str = (
        "A FastAPI service providing in-memory database operations"
    )


# Create and export settings instance
settings = Settings()
__all__ = ["settings"]

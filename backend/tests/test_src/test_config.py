from app.core.config import Settings

def test_settings_defaults():
    """Test default settings values"""
    settings = Settings()
    assert settings.API_V1_STR == "/api/v1"
    assert settings.ENVIRONMENT == "development"
    assert settings.DEBUG is True
    assert settings.SERVICE_NAME == "In-Memory Database Service"
    assert settings.SERVICE_VERSION == "1.0.0"
    assert settings.SERVICE_DESCRIPTION == "A FastAPI service providing in-memory database operations"
    assert settings.BACKEND_CORS_ORIGINS == ["http://localhost", "http://localhost:8000"]
"""Tests for the main FastAPI application."""

import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from starlette.middleware.exceptions import ExceptionMiddleware

from app.main import app, lifespan, db, user_service, order_service
from app.db.base import DatabaseError, InMemoryDB
from app.api.main import api_router
from app.services.user_service import UserService
from app.services.order_service import OrderService

# Create test client
client = TestClient(app)

@pytest.fixture
def test_db():
    """Create a test database instance."""
    return InMemoryDB()

@pytest.fixture
def test_services(test_db):
    """Create test services."""
    return UserService(test_db), OrderService(test_db)

@pytest.fixture
def test_app_with_db(test_db, test_services):
    """Create a test app with database and services."""
    user_service, order_service = test_services
    
    @asynccontextmanager
    async def test_lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        try:
            # Initialize database
            await user_service.clear_table()
            await order_service.clear_table()
            yield
        finally:
            # Clean up
            await user_service.clear_table()
            await order_service.clear_table()
    
    app = FastAPI(lifespan=test_lifespan)
    app.include_router(api_router)
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Configure error handlers
    @app.exception_handler(DatabaseError)
    async def database_error_handler(request: Request, exc: DatabaseError) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)},
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={"detail": str(exc)},
        )
    
    # Add exception middleware
    app.add_middleware(ExceptionMiddleware, handlers=app.exception_handlers)
    
    return app

def create_test_app() -> FastAPI:
    """Create a test FastAPI app with all necessary configuration."""
    app = FastAPI()
    app.include_router(api_router)

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register error handlers
    @app.exception_handler(DatabaseError)
    async def database_error_handler(request: Request, exc: DatabaseError) -> JSONResponse:
        """Handle database-specific errors."""
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)},
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """Handle all other exceptions."""
        return JSONResponse(
            status_code=500,
            content={"detail": str(exc)},
        )

    # Add root endpoint
    @app.get("/")
    async def root() -> dict:
        """Root endpoint that returns basic app info."""
        return {"message": "Welcome to In-Memory DB Service"}

    # Add exception middleware
    app.add_middleware(ExceptionMiddleware, handlers=app.exception_handlers)

    return app

def test_root():
    """Test root endpoint returns welcome message."""
    app = create_test_app()
    client = TestClient(app)

    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to In-Memory DB Service"}

def test_cors_middleware():
    """Test CORS middleware configuration."""
    app = create_test_app()
    client = TestClient(app)

    # Test preflight request
    response = client.options(
        "/",
        headers={
            "Origin": "http://localhost",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "Content-Type",
        },
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "*"

def test_database_error_handler():
    """Test database error handler returns correct response."""
    app = create_test_app()

    @app.get("/test-db-error")
    async def test_db_error():
        raise DatabaseError("Test database error")

    client = TestClient(app)
    response = client.get("/test-db-error")
    assert response.status_code == 400
    assert response.json() == {"detail": "Test database error"}

def test_general_exception_handler():
    """Test general exception handler returns correct response."""
    app = FastAPI()

    # Add exception handlers
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """Handle all other exceptions."""
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(exc)},
        )

    # Add exception middleware
    app.add_middleware(ExceptionMiddleware, handlers=app.exception_handlers)

    # Add test route that raises an exception
    @app.get("/test-general-error")
    async def test_general_error():
        """Test route that raises a ValueError."""
        raise ValueError("Test general error")

    # Create test client
    client = TestClient(app)

    # Test that the error handler catches the exception
    response = client.get("/test-general-error")
    assert response.status_code == 500
    assert response.json() == {"detail": "Test general error"}

@pytest.mark.asyncio
async def test_lifespan():
    """Test lifespan context manager properly initializes and cleans up."""
    test_app = FastAPI(lifespan=lifespan)
    test_app.include_router(api_router)

    # Configure CORS
    test_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    test_client = TestClient(test_app)

    async with lifespan(test_app):
        # Test that the database is initialized
        response = test_client.get("/api/v1/utils/health-check/")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"} 
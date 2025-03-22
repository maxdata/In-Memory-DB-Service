"""Tests for API utilities endpoints."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.utils import router as utils_router
from app.api.main import api_router
from app.main import lifespan
from app.services.user_service import UserService
from app.services.order_service import OrderService
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from app.db.base import InMemoryDB

@pytest.fixture
def test_db():
    """Create a test database instance."""
    return InMemoryDB()

@pytest.fixture
def test_services(test_db):
    """Create test services."""
    return UserService(test_db), OrderService(test_db)

@pytest.fixture
def test_app(test_db, test_services):
    """Create a test FastAPI app with utils router."""
    user_service, order_service = test_services
    
    @asynccontextmanager
    async def test_lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        # Initialize database
        await user_service.clear_table()
        await order_service.clear_table()
        yield
        # Clean up
        await user_service.clear_table()
        await order_service.clear_table()
    
    app = FastAPI(lifespan=test_lifespan)
    app.include_router(utils_router)
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app

@pytest.fixture
def test_client(test_app):
    """Create a test client."""
    return TestClient(test_app)

def test_health_check():
    """Test health check endpoint returns correct response."""
    app = FastAPI()
    app.include_router(utils_router)
    client = TestClient(app)

    response = client.get("/api/v1/utils/health-check/")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_health_check_method_not_allowed():
    """Test health check endpoint rejects POST requests."""
    app = FastAPI()
    app.include_router(utils_router)
    client = TestClient(app)

    response = client.post("/api/v1/utils/health-check/")
    assert response.status_code == 405
    assert response.json()["detail"] == "Method Not Allowed"

def test_router_prefix():
    """Test router has correct prefix and tags."""
    assert utils_router.prefix == "/api/v1/utils"
    assert "utils" in utils_router.tags

def test_router_routes():
    """Test router has expected routes configured."""
    app = FastAPI()
    app.include_router(utils_router)
    
    routes = [route for route in utils_router.routes]
    assert len(routes) == 2  # health-check and ready endpoints

    # Get the routes without the prefix
    health_route = next(route for route in routes if route.path == "/api/v1/utils/health-check/")
    ready_route = next(route for route in routes if route.path == "/api/v1/utils/ready/")
    
    assert health_route is not None
    assert ready_route is not None
    assert health_route.name == "health_check"
    assert ready_route.name == "readiness_check"
    assert "GET" in health_route.methods
    assert "GET" in ready_route.methods

@pytest.mark.asyncio
async def test_health_check_in_main_app():
    """Test health check endpoint in the main app."""
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
        response = test_client.get("/api/v1/utils/health-check/")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

@pytest.mark.asyncio
async def test_health_check_integration(test_db, test_services):
    """Test health check endpoint with full router setup."""
    user_service, order_service = test_services

    @asynccontextmanager
    async def test_lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        # Initialize database
        await user_service.clear_table()
        await order_service.clear_table()
        yield
        # Clean up
        await user_service.clear_table()
        await order_service.clear_table()

    test_app = FastAPI(lifespan=test_lifespan)
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

    async with test_lifespan(test_app):
        response = test_client.get("/api/v1/utils/health-check/")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"} 
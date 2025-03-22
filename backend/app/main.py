"""Main FastAPI application module.

This module serves as the entry point for the FastAPI application and handles:
1. Application initialization and lifecycle management
2. Database setup and sample data loading
3. CORS configuration
4. Global exception handling
5. API route registration

The initialization flow is:
1. Get singleton database instance (InMemoryDB)
2. During startup (lifespan context):
   - Clear existing tables
   - Load sample data from JSON
   - Make data available for API endpoints
3. During shutdown:
   - Clean up all tables

Sample data is loaded during startup because:
- Ensures data is available before any requests are handled
- Provides consistent initial state for testing/development
- Properly cleaned up during shutdown
- Centralizes initialization code
- Makes startup errors visible immediately
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from uuid import UUID

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .db.base import InMemoryDB, DatabaseError
from .db.initial_data import get_sample_data
from .services.user_service import UserService
from .services.order_service import OrderService
from .schemas.user import UserIn
from .schemas.order import OrderIn
from app.api.main import api_router
from app.api.v1.utils import router as utils_router

# Get singleton database instance and initialize services
db = InMemoryDB()
user_service = UserService(db)
order_service = OrderService(db)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Initialize and clean up the database.

    This lifespan manager handles the complete database lifecycle:
    1. Startup:
       - Clears any existing data in tables
       - Loads fresh sample data from JSON
       - Converts sample data to proper model instances
       - Inserts data into respective tables

    2. Runtime:
       - Database is ready with sample data
       - All API endpoints can access consistent data

    3. Shutdown:
       - Clears all tables
       - Ensures clean state for next startup

    Since we're using the singleton pattern, this lifespan manager operates on the same
    database instance that all other parts of the application use. This ensures consistent
    initialization and cleanup of the shared database state.
    """
    try:
        # Initialize database tables through services
        await user_service.clear_table()
        await order_service.clear_table()

        # Load sample data from JSON
        sample_data = get_sample_data()

        # Insert users through service layer
        for user_data in sample_data["users"]:
            # Convert to UserIn schema format
            user_in = UserIn(
                email=str(user_data["email"]),
                full_name=str(user_data["full_name"]),
                password=str(user_data.get("hashed_password", "default_password")),
                is_active=bool(user_data.get("is_active", True)),
            )
            await user_service.create_user(user_in)

        # Insert orders through service layer
        for order_data in sample_data["orders"]:
            # Convert to OrderIn schema format
            order_in = OrderIn(
                user_id=UUID(str(order_data["user_id"])),
                amount=float(order_data["total_price"]),
                description=str(order_data["product_name"]),
                status=str(order_data.get("status", "pending")),
            )
            await order_service.create_order(order_in)

        yield
    finally:
        # Clean up database on shutdown
        await user_service.clear_table()
        await order_service.clear_table()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="In-Memory DB Service",
        version="1.0.0",
        lifespan=lifespan,
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # For development, in production specify actual origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add exception handlers
    @app.exception_handler(DatabaseError)
    async def database_error_handler(
        request: Request, exc: DatabaseError
    ) -> JSONResponse:
        """Handle database errors."""
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(exc)},
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        """Handle all other exceptions."""
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(exc)},
        )

    # Register API router
    app.include_router(api_router)
    app.include_router(utils_router, prefix="/api/v1/utils")

    @app.get("/")
    async def root() -> dict[str, str]:
        """Root endpoint."""
        return {"message": "Welcome to the In-Memory Database Service"}

    return app


app = create_app()

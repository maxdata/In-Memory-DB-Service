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
from typing import Dict, Any

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .db.base import InMemoryDB, DatabaseError
from .models.user import User
from .models.order import Order
from .api.v1 import tables

# Get singleton database instance
# Even though we call InMemoryDB() here, due to the singleton pattern:
# 1. If this is the first call, it creates and initializes the instance
# 2. If the instance already exists (e.g., created by another module), it returns that instance
# This ensures we're always working with the same database instance throughout the application
db = InMemoryDB()


def get_sample_data() -> Dict[str, list[User | Order]]:
    """Get sample data for testing."""
    from uuid import uuid4
    from datetime import datetime

    user_id = uuid4()
    now = datetime.utcnow()

    user = User(
        id=user_id,
        email="test@example.com",
        full_name="Test User",
        hashed_password="hashed_password123",
        is_active=True,
        created_at=now,
        updated_at=now
    )

    order = Order(
        id=uuid4(),
        user_id=user_id,
        amount=99.99,
        description="Test Order",
        status="pending",
        created_at=now,
        updated_at=now
    )

    return {
        "users": [user],
        "orders": [order]
    }


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
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
    # Initialize database tables
    await db.clear_table("users")
    await db.clear_table("orders")

    # Load sample data
    sample_data = get_sample_data()
    for user in sample_data["users"]:
        await db.create("users", str(user.id), user.model_dump())
    for order in sample_data["orders"]:
        await db.create("orders", str(order.id), order.model_dump())

    yield
    # Clean up database
    await db.clear_table("users")
    await db.clear_table("orders")


app = FastAPI(
    title="In-Memory Database Service",
    description="A FastAPI service providing in-memory database operations",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(DatabaseError)
async def database_error_handler(_request: Request, exc: DatabaseError) -> JSONResponse:
    """Handle database exceptions."""
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )


# Include routers
app.include_router(tables.router)

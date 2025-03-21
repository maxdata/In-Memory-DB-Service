"""Main FastAPI application module."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import List, Any
from uuid import UUID

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .db.base import InMemoryDB, DatabaseError
from .services.user import UserService
from .services.order import OrderService
from .schemas.user import UserCreate, UserUpdate, UserResponse
from .schemas.order import OrderCreate, OrderUpdate, OrderResponse

# Create database instance
db = InMemoryDB()

# Create services
user_service = UserService(db)
order_service = OrderService(db)

@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Initialize and clean up the database."""
    # Initialize database tables
    db.clear_table("users")
    db.clear_table("orders")
    yield
    # Clean up database
    db.clear_table("users")
    db.clear_table("orders")

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

# User endpoints
@app.post("/api/v1/users", response_model=UserResponse)
async def create_user(user: UserCreate) -> UserResponse:
    """Create a new user."""
    return await user_service.create_user(user)

@app.get("/api/v1/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: UUID) -> UserResponse:
    """Get a user by ID."""
    return await user_service.get_user(user_id)

@app.put("/api/v1/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: UUID, user: UserUpdate) -> UserResponse:
    """Update a user."""
    return await user_service.update_user(user_id, user)

@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID) -> bool:
    """Delete a user."""
    return await user_service.delete_user(user_id)

@app.get("/api/v1/users", response_model=List[UserResponse])
async def list_users() -> List[UserResponse]:
    """List all users."""
    return await user_service.list_users()

# Order endpoints
@app.post("/api/v1/orders", response_model=OrderResponse)
async def create_order(order: OrderCreate) -> OrderResponse:
    """Create a new order."""
    return await order_service.create_order(order)

@app.get("/api/v1/orders/{order_id}", response_model=OrderResponse)
async def get_order(order_id: UUID) -> OrderResponse:
    """Get an order by ID."""
    return await order_service.get_order(order_id)

@app.put("/api/v1/orders/{order_id}", response_model=OrderResponse)
async def update_order(order_id: UUID, order: OrderUpdate) -> OrderResponse:
    """Update an order."""
    return await order_service.update_order(order_id, order)

@app.delete("/api/v1/orders/{order_id}")
async def delete_order(order_id: UUID) -> bool:
    """Delete an order."""
    return await order_service.delete_order(order_id)

@app.get("/api/v1/orders", response_model=List[OrderResponse])
async def list_orders() -> List[OrderResponse]:
    """List all orders."""
    return await order_service.list_orders()

@app.get("/api/v1/users/{user_id}/orders", response_model=List[OrderResponse])
async def get_user_orders(user_id: UUID) -> List[OrderResponse]:
    """Get all orders for a specific user."""
    return await order_service.get_user_orders(user_id)

# TDOO: 

@app.get("/api/v1/tables/join", response_model=list[dict[str, Any]])
async def join_tables(
    table1: str, table2: str, key: str
) -> list[dict[str, dict[str, Any]]]:
    """
    Join two tables based on a common key.

    Args:
        table1: Name of the first table
        table2: Name of the second table
        key: Common key to join on

    Returns:
        List of joined records
    """
    try:
        return db.join_tables(table1, table2, key)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/v1/tables/{table}/dump", response_model=list[dict[str, Any]])
async def dump_table(table: str) -> list[dict[str, Any]]:
    """
    Dump all contents of the specified table.

    Args:
        table: Name of the table to dump

    Returns:
        List of all records in the table
    """
    try:
        return db.dump_table(table)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

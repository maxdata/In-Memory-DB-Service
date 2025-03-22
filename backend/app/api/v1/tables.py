from typing import Dict
from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends

from app.api.deps import UserServiceDep, OrderServiceDep
from app.db.base import InMemoryDB, RecordNotFoundError
from app.schemas.user import UserIn, UserOut, UsersOut
from app.schemas.order import OrderIn, OrderOut, OrdersOut


router = APIRouter(prefix="/api/v1", tags=["tables"])


# User endpoints
@router.post("/users", response_model=UserOut)
async def create_user(
    user: UserIn,
    user_service: UserServiceDep
) -> UserOut:
    """Create a new user."""
    return await user_service.create_user(user)


@router.get("/users/{user_id}", response_model=UserOut)
async def get_user(
    user_id: UUID,
    user_service: UserServiceDep
) -> UserOut:
    """Get a user by ID."""
    try:
        return await user_service.get_user(user_id)
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")


@router.get("/users", response_model=UsersOut)
async def list_users(
    user_service: UserServiceDep
) -> UsersOut:
    """List all users."""
    users = await user_service.list_users()
    return UsersOut(data=users, count=len(users))


# Order endpoints
@router.post("/orders", response_model=OrderOut)
async def create_order(
    order: OrderIn,
    order_service: OrderServiceDep,
    user_service: UserServiceDep
) -> OrderOut:
    """Create a new order."""
    # Verify user exists
    try:
        await user_service.get_user(order.user_id)
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    
    return await order_service.create_order(order)


@router.get("/orders/{order_id}", response_model=OrderOut)
async def get_order(
    order_id: UUID,
    order_service: OrderServiceDep
) -> OrderOut:
    """Get an order by ID."""
    try:
        return await order_service.get_order(order_id)
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Order not found")


@router.get("/users/{user_id}/orders", response_model=OrdersOut)
async def get_user_orders(
    user_id: UUID,
    user_service: UserServiceDep,
    order_service: OrderServiceDep
) -> OrdersOut:
    """Get all orders for a user."""
    # Verify user exists
    try:
        await user_service.get_user(user_id)
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    
    orders = await order_service.get_user_orders(user_id)
    return OrdersOut(data=orders, count=len(orders))


@router.get("/orders/{order_id}/user", response_model=UserOut)
async def get_order_user(
    order_id: UUID,
    order_service: OrderServiceDep,
    user_service: UserServiceDep
) -> UserOut:
    """Get the user associated with an order."""
    try:
        order = await order_service.get_order(order_id)
        return await user_service.get_user(order.user_id)
    except RecordNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Generic table operations
@router.get("/tables/{table}/dump")
async def dump_table(
    table: str, 
    db: InMemoryDB = Depends(get_memory_db)
) -> Dict:
    """Dump all records from a table."""
    if table not in ["users", "orders"]:
        raise HTTPException(status_code=404, detail=f"Table {table} not found")
    
    data = await db.list(table)
    return {
        "data": data,
        "count": len(data),
    }

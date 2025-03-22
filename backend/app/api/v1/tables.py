from typing import Any, Annotated, List, Dict
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from app.api.deps import get_memory_db
from app.db.base import InMemoryDB, RecordNotFoundError
from app.models.user import Order, User
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse

router = APIRouter(prefix="/api/v1", tags=["tables"])

# Map table names to their corresponding models
TABLE_MODELS = {"users": User, "orders": Order}


# Generic record creation model
class GenericCreate(BaseModel):
    data: dict[str, Any]


# User endpoints
@router.post("/users", response_model=UserResponse)
async def create_user(
    *, db: Annotated[InMemoryDB, Depends(get_memory_db)], user: UserCreate
) -> UserResponse:
    """Create a new user."""
    return await db.add_user(user)


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    *, db: Annotated[InMemoryDB, Depends(get_memory_db)], user_id: UUID
) -> UserResponse:
    """Get a user by ID."""
    try:
        user = await db.get_user(user_id)
        return UserResponse(**user)
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")


@router.patch("/users/{user_id}", response_model=UserResponse)
async def update_user(
    *,
    db: Annotated[InMemoryDB, Depends(get_memory_db)],
    user_id: UUID,
    user: UserUpdate,
) -> UserResponse:
    """Update a user."""
    try:
        updated_user = await db.update_user(user_id, user)
        return UserResponse(**updated_user)
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")


@router.delete("/users/{user_id}")
async def delete_user(
    *, db: Annotated[InMemoryDB, Depends(get_memory_db)], user_id: UUID
) -> bool:
    """Delete a user."""
    try:
        return await db.delete_user(user_id)
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")


@router.get("/users", response_model=List[UserResponse])
async def list_users(
    db: Annotated[InMemoryDB, Depends(get_memory_db)],
) -> List[UserResponse]:
    """List all users."""
    users = await db.list("users")
    return [UserResponse(**user) for user in users]


# Order endpoints
@router.post("/orders", response_model=OrderResponse)
async def create_order(
    *, db: Annotated[InMemoryDB, Depends(get_memory_db)], order: OrderCreate
) -> OrderResponse:
    """Create a new order."""
    try:
        # First check if user exists
        await db.get_user(order.user_id)
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        print(f"Error checking user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error checking user: {str(e)}")

    try:
        # Generate UUID for the order if not provided
        if not hasattr(order, "id"):
            order.id = uuid4()

        print(f"Creating order with data: {order.model_dump()}")  # Debug log
        result = await db.add_order(order)
        print(f"Created order: {result}")  # Debug log
        return OrderResponse(**result)
    except Exception as e:
        print(f"Error creating order: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating order: {str(e)}")


@router.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(
    *, db: Annotated[InMemoryDB, Depends(get_memory_db)], order_id: UUID
) -> OrderResponse:
    """Get an order by ID."""
    try:
        order = await db.get_order(order_id)
        if not order:
            raise RecordNotFoundError()
        return OrderResponse(**order)
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Order not found")


@router.patch("/orders/{order_id}", response_model=OrderResponse)
async def update_order(
    *,
    db: Annotated[InMemoryDB, Depends(get_memory_db)],
    order_id: UUID,
    order: OrderUpdate,
) -> OrderResponse:
    """Update an order."""
    updated_order = await db.update_order(order_id, order)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order


@router.delete("/orders/{order_id}")
async def delete_order(
    *, db: Annotated[InMemoryDB, Depends(get_memory_db)], order_id: UUID
) -> bool:
    """Delete an order."""
    success = await db.delete_order(order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return success


@router.get("/orders", response_model=List[OrderResponse])
async def list_orders(
    db: Annotated[InMemoryDB, Depends(get_memory_db)],
) -> List[OrderResponse]:
    """List all orders."""
    orders = await db.list("orders")
    return [OrderResponse(**order) for order in orders]


@router.get("/users/{user_id}/orders", response_model=List[OrderResponse])
async def get_user_orders(
    *, db: Annotated[InMemoryDB, Depends(get_memory_db)], user_id: UUID
) -> List[OrderResponse]:
    """Get all orders for a specific user."""
    # First check if user exists
    try:
        await db.get_user(user_id)
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")

    # Get all orders
    orders = await db.list_orders()
    # Filter orders for this user - convert both to strings for comparison
    user_orders = [
        order for order in orders if str(order.get("user_id")) == str(user_id)
    ]
    return [OrderResponse(**order) for order in user_orders]


@router.get("/orders/{order_id}/user", response_model=UserResponse)
async def get_order_user(
    *, db: Annotated[InMemoryDB, Depends(get_memory_db)], order_id: UUID
) -> UserResponse:
    """Get user details for a specific order."""
    # First check if order exists and get its user_id
    try:
        order = await db.get_order(order_id)
        if not order:
            raise RecordNotFoundError()

        # Get the user_id from the order
        user_id = order.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=404, detail="No user associated with this order"
            )

        try:
            # Get the user details - ensure user_id is a UUID
            user_id_uuid = user_id if isinstance(user_id, UUID) else UUID(user_id)
            user = await db.get_user(user_id_uuid)
            return UserResponse(**user)
        except RecordNotFoundError:
            raise HTTPException(status_code=404, detail="Associated user not found")
        except ValueError:
            raise HTTPException(
                status_code=500, detail="Invalid user ID format in order"
            )
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Order not found")


# Generic table operations
@router.get("/tables/{table}/dump", response_model=Dict[str, Any])
async def dump_table(
    table: str, db: InMemoryDB = Depends(get_memory_db)
) -> Dict[str, Any]:
    """
    Dump all records from a table.
    """
    if table == "users":
        data = await db.list_users()
        return {
            "data": data,
            "count": len(data),
        }
    elif table == "orders":
        data = await db.list_orders()
        return {
            "data": data,
            "count": len(data),
        }
    else:
        raise HTTPException(status_code=404, detail=f"Table {table} not found")

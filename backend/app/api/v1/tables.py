"""
API routes for table operations.

This module provides REST endpoints for:
1. User CRUD operations
2. Order CRUD operations
3. User-Order relationships
4. Table-level operations
5. System health operations

All routes use dependency injection for services and follow REST best practices.
"""

from typing import Dict, Sequence, Union, List
from uuid import UUID

from fastapi import APIRouter, HTTPException, status, Path

from app.api.deps import UserServiceDep, OrderServiceDep
from app.db.base import RecordNotFoundError, InMemoryDB
from app.schemas.user import UserIn, UserOut, UsersOut, UserUpdate
from app.schemas.order import OrderIn, OrderOut, OrdersOut, OrderUpdate


router = APIRouter(prefix="/api/v1", tags=["v1"])
db = InMemoryDB()


# User endpoints
@router.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserIn, user_service: UserServiceDep) -> UserOut:
    """
    Create a new user.

    Args:
        user: User data for creation
        user_service: Injected user service dependency

    Returns:
        UserOut: Created user data

    Raises:
        HTTPException: If user creation fails
    """
    try:
        return await user_service.create_user(user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/users/{user_id}", response_model=UserOut)
async def get_user(user_id: UUID, user_service: UserServiceDep) -> UserOut:
    """
    Get a user by ID.

    Args:
        user_id: UUID of the user to retrieve
        user_service: Injected user service dependency

    Returns:
        UserOut: User data

    Raises:
        HTTPException: If user is not found
    """
    try:
        return await user_service.get_user(user_id)
    except RecordNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found"
        )


@router.get("/users", response_model=UsersOut)
async def list_users(user_service: UserServiceDep) -> UsersOut:
    """
    List all users.

    Args:
        user_service: Injected user service dependency

    Returns:
        UsersOut: List of users with count
    """
    users = await user_service.list_users()
    return UsersOut(data=users, count=len(users))


@router.patch("/users/{user_id}", response_model=UserOut)
async def update_user(
    user_id: UUID, user: UserUpdate, user_service: UserServiceDep
) -> UserOut:
    """
    Update a user by ID.

    Args:
        user_id: UUID of the user to update
        user: Updated user data (partial updates allowed)
        user_service: Injected user service dependency

    Returns:
        UserOut: Updated user data

    Raises:
        HTTPException: If user is not found
    """
    try:
        return await user_service.update_user(user_id, user)
    except RecordNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found"
        )


@router.delete("/users/{user_id}", response_model=bool)
async def delete_user(user_id: UUID, user_service: UserServiceDep) -> bool:
    """
    Delete a user by ID.

    Args:
        user_id: UUID of the user to delete
        user_service: Injected user service dependency

    Returns:
        bool: True if user was deleted

    Raises:
        HTTPException: If user is not found
    """
    try:
        return await user_service.delete_user(user_id)
    except RecordNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found"
        )


# Order endpoints
@router.post("/orders", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
async def create_order(
    order: OrderIn, order_service: OrderServiceDep, user_service: UserServiceDep
) -> OrderOut:
    """
    Create a new order.

    Args:
        order: Order data for creation
        order_service: Injected order service dependency
        user_service: Injected user service dependency for validation

    Returns:
        OrderOut: Created order data

    Raises:
        HTTPException: If user not found or order creation fails
    """
    try:
        # Verify user exists
        await user_service.get_user(order.user_id)
        return await order_service.create_order(order)
    except RecordNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {order.user_id} not found",
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/orders/{order_id}", response_model=OrderOut)
async def get_order(order_id: UUID, order_service: OrderServiceDep) -> OrderOut:
    """
    Get an order by ID.

    Args:
        order_id: UUID of the order to retrieve
        order_service: Injected order service dependency

    Returns:
        OrderOut: Order data

    Raises:
        HTTPException: If order is not found
    """
    try:
        return await order_service.get_order(order_id)
    except RecordNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Order {order_id} not found"
        )


@router.get("/users/{user_id}/orders", response_model=OrdersOut)
async def get_user_orders(
    user_id: UUID, user_service: UserServiceDep, order_service: OrderServiceDep
) -> OrdersOut:
    """
    Get all orders for a user.

    Args:
        user_id: UUID of the user whose orders to retrieve
        user_service: Injected user service dependency for validation
        order_service: Injected order service dependency

    Returns:
        OrdersOut: List of user's orders with count

    Raises:
        HTTPException: If user is not found
    """
    try:
        # Verify user exists
        await user_service.get_user(user_id)
        orders = await order_service.get_user_orders(user_id)
        return OrdersOut(data=orders, count=len(orders))
    except RecordNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found"
        )


@router.get("/orders/{order_id}/user", response_model=UserOut)
async def get_order_user(
    order_id: UUID, order_service: OrderServiceDep, user_service: UserServiceDep
) -> UserOut:
    """
    Get the user associated with an order.

    Args:
        order_id: UUID of the order
        order_service: Injected order service dependency
        user_service: Injected user service dependency

    Returns:
        UserOut: User data for the order's owner

    Raises:
        HTTPException: If order or user is not found
    """
    try:
        order = await order_service.get_order(order_id)
        return await user_service.get_user(order.user_id)
    except RecordNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/orders", response_model=OrdersOut)
async def list_orders(order_service: OrderServiceDep) -> OrdersOut:
    """
    List all orders.

    Args:
        order_service: Injected order service dependency

    Returns:
        OrdersOut: List of orders with count
    """
    orders = await order_service.list_orders()
    return OrdersOut(data=orders, count=len(orders))


@router.patch("/orders/{order_id}", response_model=OrderOut)
async def update_order(
    order_id: UUID, order: OrderUpdate, order_service: OrderServiceDep
) -> OrderOut:
    """
    Update an order by ID.

    Args:
        order_id: UUID of the order to update
        order: Updated order data (partial updates allowed)
        order_service: Injected order service dependency

    Returns:
        OrderOut: Updated order data

    Raises:
        HTTPException: If order is not found
    """
    try:
        # Convert Pydantic model to dict, excluding unset and None values
        order_data = order.model_dump(exclude_unset=True, exclude_none=True)
        return await order_service.update_order(order_id, order_data)
    except RecordNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Order {order_id} not found"
        )


@router.delete("/orders/{order_id}", response_model=bool)
async def delete_order(order_id: UUID, order_service: OrderServiceDep) -> bool:
    """
    Delete an order by ID.

    Args:
        order_id: UUID of the order to delete
        order_service: Injected order service dependency

    Returns:
        bool: True if order was deleted

    Raises:
        HTTPException: If order is not found
    """
    try:
        return await order_service.delete_order(order_id)
    except RecordNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Order {order_id} not found"
        )


# Generic table operations
@router.get("/tables/{table_name}/dump", response_model=Dict[str, object])
async def dump_table(
    table_name: str,
    user_service: UserServiceDep,
    order_service: OrderServiceDep,
    format: str = "json",
) -> Dict[str, object]:
    """
    Dump all records from a table.

    This endpoint is intended for debugging and development purposes.
    In production, it should be protected by appropriate authentication
    and authorization mechanisms.

    Args:
        table_name: Name of the table to dump (either "users" or "orders")
        format: Output format (only "json" supported)
        user_service: Injected user service dependency
        order_service: Injected order service dependency

    Returns:
        Dict containing:
            - data: List of records from the table
            - count: Total number of records

    Raises:
        HTTPException: If operation fails or table name is invalid
    """
    if format != "json":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid format. Only 'json' is supported",
        )

    try:
        data: Sequence[Union[UserOut, OrderOut]]
        if table_name == "users":
            data = await user_service.list_users(bulk_mode=True)
        elif table_name == "orders":
            data = await order_service.list_orders(bulk_mode=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Table {table_name} not found",
            )

        return {"data": data, "count": len(data)}
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to dump table {table_name}: {str(e)}",
        )


@router.get("/db/dump/{table_name}", response_model=List[Dict[str, object]])
async def dump_table_raw(table_name: str = Path(...)) -> List[Dict[str, object]]:
    """
    Dump all records from a table in raw format.

    Args:
        table_name: Name of the table to dump

    Returns:
        List[Dict[str, object]]: Raw records from the table

    Raises:
        HTTPException: If table does not exist
    """
    if not await db.table_exists(table_name):
        raise HTTPException(status_code=404, detail=f"Table {table_name} not found")
    return await db.list_records(table_name)


@router.delete("/tables/{table_name}", response_model=bool)
async def clear_table(
    table_name: str,
    user_service: UserServiceDep,
    order_service: OrderServiceDep,
) -> bool:
    """
    Clear all records from a table.

    Args:
        table_name: Name of the table to clear (either "users" or "orders")
        user_service: Injected user service dependency
        order_service: Injected order service dependency

    Returns:
        bool: True if table was cleared

    Raises:
        HTTPException: If table name is invalid
    """
    try:
        if table_name == "users":
            await user_service.clear_table()
        elif table_name == "orders":
            await order_service.clear_table()
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Table {table_name} not found",
            )
        return True
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear table {table_name}: {str(e)}",
        )


# System health endpoints
@router.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint.
    Returns 200 OK if the service is healthy.

    Returns:
        Dict[str, str]: Health status
    """
    return {"status": "healthy"}


@router.get("/ready")
async def readiness_check() -> Dict[str, str]:
    """
    Readiness check endpoint.
    Returns 200 OK if the service is ready to accept requests.

    Returns:
        Dict[str, str]: Readiness status
    """
    # Here you might want to add additional checks like database connectivity
    return {"status": "ready"}

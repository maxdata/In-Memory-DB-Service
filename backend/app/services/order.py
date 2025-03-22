"""
CRUD operations for the in-memory database service.
"""

from typing import Any, TypeVar, List, Optional
from uuid import UUID, uuid4

from app.db import db
from app.models.order import Order, OrderCreate, OrderResponse
from app.db.base import InMemoryDB

T = TypeVar("T")


class OrderService:
    """
    Service for managing order operations.
    """

    def __init__(self, db_instance: InMemoryDB = None):
        """
        Initialize the service with a database instance.
        """
        self.db = db_instance or db

    async def create_order(self, order_data: OrderCreate) -> OrderResponse:
        """
        Create a new order.

        Args:
            order_data: Order data to create

        Returns:
            OrderResponse: Created order data
        """
        order_dict = order_data.model_dump()
        order_dict["id"] = uuid4()
        order = Order(**order_dict)
        result = await self.db.add_order(order)
        return OrderResponse(**result)

    async def get_order(self, order_id: UUID) -> Optional[OrderResponse]:
        """
        Get an order by ID.

        Args:
            order_id: Order ID to get

        Returns:
            Optional[OrderResponse]: Order data if found
        """
        try:
            result = await self.db.get_order(order_id)
            return OrderResponse(**result)
        except Exception:
            return None

    async def update_order(self, order_id: UUID, order_data: dict) -> Optional[OrderResponse]:
        """
        Update an order.

        Args:
            order_id: Order ID to update
            order_data: Order data to update

        Returns:
            Optional[OrderResponse]: Updated order data
        """
        try:
            result = await self.db.update_order(order_id, order_data)
            return OrderResponse(**result)
        except Exception:
            return None

    async def delete_order(self, order_id: UUID) -> bool:
        """
        Delete an order.

        Args:
            order_id: Order ID to delete

        Returns:
            bool: True if deletion was successful
        """
        try:
            return await self.db.delete_order(order_id)
        except Exception:
            return False

    async def list_orders(self) -> List[OrderResponse]:
        """
        List all orders.

        Returns:
            List[OrderResponse]: List of orders
        """
        try:
            results = await self.db.list_orders()
            return [OrderResponse(**order) for order in results]
        except Exception:
            return []

    async def get_user_orders(self, user_id: UUID) -> List[OrderResponse]:
        """
        Get all orders for a specific user.

        Args:
            user_id: User ID to get orders for

        Returns:
            List[OrderResponse]: List of orders for the user
        """
        try:
            results = await self.db.get_user_orders(user_id)
            return [OrderResponse(**order) for order in results]
        except Exception:
            return []


def create_order(*, data: dict[str, Any]) -> Order:
    """Create a new order in the in-memory database."""
    order = Order(**data)
    db.add_order(order)
    return order


def get_order(*, order_id: UUID) -> Optional[Order]:
    """Get an order by ID from the in-memory database."""
    return db.get_order(order_id)


def update_order(*, order_id: UUID, data: dict[str, Any]) -> Optional[Order]:
    """Update an order in the in-memory database."""
    return db.update_order(order_id, data)


def delete_order(*, order_id: UUID) -> bool:
    """Delete an order from the in-memory database."""
    return db.delete_order(order_id)


def list_orders() -> list[Order]:
    """List all orders in the in-memory database."""
    return db.list_orders()

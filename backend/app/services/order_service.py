"""Service layer for handling order-related operations."""

from typing import List, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime, UTC

from app.db.base import InMemoryDB, RecordNotFoundError, DatabaseError
from app.schemas.order import OrderIn, OrderOut
from .base_service import BaseService


class OrderService(BaseService):
    """Service layer for handling order-related operations"""

    def __init__(self, db: InMemoryDB):
        super().__init__(db, "orders")

    async def create_order(self, order_data: OrderIn) -> OrderOut:
        """Create a new order"""
        # Create order dict with generated fields
        order_dict = order_data.model_dump()
        order_dict["id"] = str(
            uuid4()
        )  # Store ID as string since that's what DB expects
        now = datetime.now(UTC)
        order_dict["created_at"] = now
        order_dict["updated_at"] = now

        # Store in DB
        record_id = await self.db.create_record(self.table_name, order_dict)
        stored_order = await self.db.get_record(self.table_name, record_id)
        if not stored_order:
            raise DatabaseError("Failed to retrieve created order")
        return OrderOut(**stored_order)

    async def get_order(self, order_id: UUID) -> OrderOut:
        """Get an order by ID"""
        order = await self.db.get_record(self.table_name, order_id)
        if not order:
            raise RecordNotFoundError(f"Order with ID {order_id} not found")
        return OrderOut(**order)

    async def update_order(
        self, order_id: UUID, order_data: Dict[str, Any]
    ) -> OrderOut:
        """Update an order's data"""
        # Get current order data
        current_order = await self.db.get_record(self.table_name, order_id)
        if not current_order:
            raise RecordNotFoundError(f"Order with ID {order_id} not found")

        # Update with new data
        update_data = {k: v for k, v in order_data.items() if v is not None}
        order_dict = {
            **current_order,
            **update_data,
            "updated_at": datetime.now(UTC),
        }

        success = await self.db.update_record(self.table_name, order_id, order_dict)
        if not success:
            raise DatabaseError(f"Failed to update order with ID {order_id}")

        # Fetch and return updated order
        updated_order = await self.db.get_record(self.table_name, order_id)
        if not updated_order:
            raise DatabaseError(f"Failed to retrieve updated order with ID {order_id}")
        return OrderOut(**updated_order)

    async def delete_order(self, order_id: UUID) -> bool:
        """Delete an order"""
        success = await self.db.delete_record(self.table_name, order_id)
        if not success:
            raise RecordNotFoundError(f"Order with ID {order_id} not found")
        return True

    async def list_orders(self, bulk_mode: bool = False) -> List[OrderOut]:
        """
        List all orders.

        Args:
            bulk_mode: If True, uses optimized bulk retrieval (Note: base DB doesn't support this yet)
        """
        orders = await self.db.list_records(self.table_name)
        return [OrderOut.model_validate(order) for order in orders]

    async def get_user_orders(
        self, user_id: UUID, bulk_mode: bool = False
    ) -> List[OrderOut]:
        """
        Get all orders for a specific user.

        Args:
            user_id: The user ID to filter orders by
            bulk_mode: If True, uses optimized bulk retrieval (Note: base DB doesn't support this yet)
        """
        orders = await self.db.list_records(self.table_name)
        user_orders = [
            order for order in orders if str(order.get("user_id")) == str(user_id)
        ]
        return [OrderOut.model_validate(order) for order in user_orders]

from typing import Dict, List, Any
from uuid import UUID, uuid4

from app.models.order import Order
from app.db.base import InMemoryDB


class OrderService:
    """Service layer for handling order-related operations"""

    def __init__(self, db: InMemoryDB):
        self.db = db
        self.table_name = "orders"

    async def create_order(self, order_data: Order) -> Dict[str, Any]:
        """Create a new order"""
        order_dict = order_data.model_dump()
        order_id = str(order_dict.get("id", uuid4()))
        return await self.db.create(self.table_name, order_id, order_dict)

    async def get_order(self, order_id: UUID) -> Dict[str, Any]:
        """Get an order by ID"""
        return await self.db.read(self.table_name, str(order_id))

    async def update_order(self, order_id: UUID, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an order's data"""
        update_data = order_data.copy()
        update_data["id"] = str(order_id)  # Preserve the order's ID
        return await self.db.update(self.table_name, str(order_id), update_data)

    async def delete_order(self, order_id: UUID) -> bool:
        """Delete an order by ID"""
        return await self.db.delete(self.table_name, str(order_id))

    async def list_orders(self) -> List[Dict[str, Any]]:
        """List all orders"""
        return await self.db.list(self.table_name)

    async def get_user_orders(self, user_id: UUID) -> List[Dict[str, Any]]:
        """Get all orders for a specific user"""
        orders = await self.list_orders()
        return [order for order in orders if order.get("user_id") == str(user_id)] 
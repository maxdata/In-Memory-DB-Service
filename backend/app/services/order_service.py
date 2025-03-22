from typing import List, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime

from app.db.base import InMemoryDB, RecordNotFoundError
from app.schemas.order import OrderCreate, OrderUpdate, OrderInDB, OrderResponse


class OrderService:
    """Service layer for handling order-related operations"""

    def __init__(self, db: InMemoryDB):
        self.db = db
        self.table_name = "orders"

    async def create_order(self, order_data: OrderCreate) -> OrderResponse:
        """Create a new order"""
        # Create order dict with generated fields
        order_dict = order_data.model_dump()
        order_dict["id"] = uuid4()
        order_dict["created_at"] = datetime.utcnow()
        order_dict["updated_at"] = datetime.utcnow()

        # Store in DB
        stored_order = await self.db.create(self.table_name, str(order_dict["id"]), order_dict)
        return OrderResponse(**stored_order)

    async def get_order(self, order_id: UUID) -> OrderResponse:
        """Get an order by ID"""
        order = await self.db.read(self.table_name, str(order_id))
        return OrderResponse(**order)

    async def update_order(self, order_id: UUID, order_data: OrderUpdate) -> OrderResponse:
        """Update an order's data"""
        # Get current order data
        current_order = await self.db.read(self.table_name, str(order_id))
        
        # Update with new data
        update_data = order_data.model_dump(exclude_unset=True)
        order_dict = {**current_order, **update_data, "updated_at": datetime.utcnow()}
        updated_order = await self.db.update(self.table_name, str(order_id), order_dict)
        return OrderResponse(**updated_order)

    async def delete_order(self, order_id: UUID) -> bool:
        """Delete an order"""
        return await self.db.delete(self.table_name, str(order_id))

    async def list_orders(self) -> List[OrderResponse]:
        """List all orders"""
        orders = await self.db.list(self.table_name)
        return [OrderResponse(**order) for order in orders]

    async def get_user_orders(self, user_id: UUID) -> List[OrderResponse]:
        """Get all orders for a specific user"""
        orders = await self.db.list(self.table_name)
        user_orders = [order for order in orders if str(order.get("user_id")) == str(user_id)]
        return [OrderResponse(**order) for order in user_orders] 
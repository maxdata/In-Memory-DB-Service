"""
CRUD operations for the in-memory database service.
"""

from typing import Any, TypeVar, List
from uuid import UUID

from backend.app.db import db
from backend.app.model.order import Order
from ..db.base import InMemoryDB
from ..schemas.order import OrderCreate, OrderUpdate, OrderResponse

# Define a generic type for models
ModelT = TypeVar("ModelT", Order)

# In-memory storage using dictionaries
tables: dict[str, dict[str, dict[str, Any]]] = {"orders": {}}

class OrderService:
    def __init__(self, db: InMemoryDB):
        self.db = db
        self.table = "orders"

    async def create_order(self, order: OrderCreate) -> OrderResponse:
        order_data = order.model_dump()
        await self.db.create(self.table, str(order.id), order_data)
        return OrderResponse(**order_data)

    async def get_order(self, order_id: UUID) -> OrderResponse:
        order_data = await self.db.read(self.table, str(order_id))
        return OrderResponse(**order_data)

    async def update_order(self, order_id: UUID, order: OrderUpdate) -> OrderResponse:
        update_data = {k: v for k, v in order.model_dump().items() if v is not None}
        order_data = await self.db.update(self.table, str(order_id), update_data)
        return OrderResponse(**order_data)

    async def delete_order(self, order_id: UUID) -> bool:
        return await self.db.delete(self.table, str(order_id))

    async def list_orders(self) -> List[OrderResponse]:
        orders = await self.db.list(self.table)
        return [OrderResponse(**order) for order in orders]

    async def get_user_orders(self, user_id: UUID) -> List[OrderResponse]:
        orders = await self.db.join("users", self.table, "user_id")
        return [OrderResponse(**order) for order in orders if order["user_id"] == str(user_id)]

def create_order(*, data: dict[str, Any]) -> Order:
    """Create a new order in the in-memory database."""
    order = Order(**data)
    db.add_record("orders", str(order.id), order.model_dump())
    return order


def get_order(*, order_id: UUID) -> Order | None:
    """Get an order by ID from the in-memory database."""
    result = db.get_record("orders", str(order_id))
    return Order(**result) if result else None


def update_order(*, order_id: UUID, data: dict[str, Any]) -> Order | None:
    """Update an order in the in-memory database."""
    result = db.update_record("orders", str(order_id), data)
    return Order(**result) if result else None


def delete_order(*, order_id: UUID) -> bool:
    """Delete an order from the in-memory database."""
    return db.delete_record("orders", str(order_id))


def list_orders() -> list[Order]:
    """List all orders in the in-memory database."""
    return [Order(**order_data) for order_data in db.dump_table("orders")]

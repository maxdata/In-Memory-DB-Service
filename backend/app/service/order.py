"""
CRUD operations for the in-memory database service.
"""

from typing import Any, TypeVar
from uuid import UUID

from backend.app.db import db

from backend.app.model.order import Order

# Define a generic type for models
ModelT = TypeVar("ModelT", Order)

# In-memory storage using dictionaries
tables: dict[str, dict[str, dict[str, Any]]] = {"orders": {}}

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

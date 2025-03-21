from typing import Dict
from uuid import UUID

from app.models import InMemoryDB, User, Order
from app.initial_data import get_sample_data

# Global in-memory database instance
memory_db = InMemoryDB()

def init_db() -> None:
    """
    Initialize the in-memory database with sample data.
    This is useful for testing and development.
    """
    # Clear existing data
    memory_db.users.clear()
    memory_db.orders.clear()

    # Get sample data
    sample_data = get_sample_data()
    
    # Add users
    for user_data in sample_data["users"]:
        user = User(**user_data)
        memory_db.add_user(user)
    
    # Add orders
    for order_data in sample_data["orders"]:
        order = Order(**order_data)
        memory_db.add_order(order)


def get_db() -> InMemoryDB:
    """
    Get the in-memory database instance.
    This is a simple getter since we're using a global instance.
    """
    return memory_db

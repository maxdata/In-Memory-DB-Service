"""Sample data for testing the in-memory database service."""

from datetime import datetime
from uuid import uuid4

# Sample users
SAMPLE_USERS = [
    {
        "id": str(uuid4()),
        "email": "john.doe@example.com",
        "full_name": "John Doe",
        "age": 30,
        "is_active": True,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    },
    {
        "id": str(uuid4()),
        "email": "jane.smith@example.com",
        "full_name": "Jane Smith",
        "age": 25,
        "is_active": True,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }
]

# Sample orders
SAMPLE_ORDERS = [
    {
        "id": str(uuid4()),
        "user_id": SAMPLE_USERS[0]["id"],
        "product_name": "Laptop",
        "quantity": 1,
        "total_price": 999.99,
        "status": "processing",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    },
    {
        "id": str(uuid4()),
        "user_id": SAMPLE_USERS[0]["id"],
        "product_name": "Mouse",
        "quantity": 2,
        "total_price": 49.98,
        "status": "shipped",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    },
    {
        "id": str(uuid4()),
        "user_id": SAMPLE_USERS[1]["id"],
        "product_name": "Keyboard",
        "quantity": 1,
        "total_price": 129.99,
        "status": "pending",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }
]

def get_sample_data():
    """Get sample data for the database."""
    return {
        "users": SAMPLE_USERS,
        "orders": SAMPLE_ORDERS
    }

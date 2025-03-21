"""Test helper functions for the in-memory database service."""

from uuid import uuid4
from datetime import datetime
from typing import Dict, Any

from app.models import User, Order

def create_test_user(email: str = None) -> dict:
    """Create a test user with random data.
    
    Args:
        email: Optional email to use. If not provided, a random one will be generated.
        
    Returns:
        Dictionary containing user data.
    """
    if email is None:
        email = f"test_{uuid4()}@example.com"
    
    return {
        "email": email,
        "password": "testpassword123",
        "full_name": f"Test User {uuid4().hex[:8]}"
    }

def create_test_order(user_id: str) -> dict:
    """Create a test order with random data.
    
    Args:
        user_id: ID of the user placing the order.
        
    Returns:
        Dictionary containing order data.
    """
    return {
        "user_id": user_id,
        "product_name": f"Test Product {uuid4().hex[:8]}",
        "quantity": 1,
        "price": 9.99,
        "status": "pending"
    }

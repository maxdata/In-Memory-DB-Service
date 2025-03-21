from collections.abc import Generator
from typing import Dict

import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from app.core.db import memory_db, init_db
from app.main import app
from app.models import User, Order, UserCreate
from tests.test_utils import random_lower_string


@pytest.fixture(scope="function", autouse=True)
def setup_test_db() -> Generator[Dict, None, None]:
    """Initialize a clean in-memory database for each test.
    
    This fixture runs automatically before each test function and provides:
    1. A clean database state
    2. Sample test data
    3. Cleanup after the test
    
    Returns:
        Dict containing test data references for use in tests
    """
    # Clear existing data
    memory_db.users.clear()
    memory_db.orders.clear()
    
    # Initialize with minimal test data
    init_db()
    
    # Create a test user for general use
    test_user = UserCreate(
        email="test@example.com",
        password=random_lower_string(),
        full_name="Test User"
    )
    
    # Add test user to database
    memory_db.add_user(test_user)
    
    yield {"test_user": test_user}
    
    # Cleanup after test
    memory_db.users.clear()
    memory_db.orders.clear()


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    """Create a test client for making API requests."""
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
def test_user(setup_test_db: Dict) -> User:
    """Create and return a test user for use in tests."""
    from app import crud
    user = crud.create_user(data=setup_test_db["test_user"])
    return user


@pytest.fixture(scope="function")
def test_order(test_user: User) -> Order:
    """Create and return a test order linked to the test user."""
    from app import crud
    order_data = {
        "product": "Test Product",
        "quantity": 1,
        "user_id": str(test_user.id)
    }
    order = crud.create_order(data=order_data)
    return order


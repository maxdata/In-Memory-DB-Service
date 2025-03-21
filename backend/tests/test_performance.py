"""Performance tests for the in-memory database service."""

import time
from fastapi.testclient import TestClient

from app.core.config import settings
from .test_helpers import create_test_user, create_test_order


def test_bulk_operations(client: TestClient, setup_test_db):
    """Test performance of bulk operations."""
    # Test bulk user creation
    start_time = time.time()
    users = []
    for _ in range(100):
        user_data = create_test_user()
        response = client.post(
            f"{settings.API_V1_STR}/tables/users/records",
            json=user_data
        )
        assert response.status_code == 200
        users.append(response.json())
    user_creation_time = time.time() - start_time
    assert user_creation_time < 2.0  # Should create 100 users in under 2 seconds

    # Test bulk order creation
    start_time = time.time()
    for user in users[:50]:  # Create orders for half of the users
        order_data = create_test_order(user["id"])
        response = client.post(
            f"{settings.API_V1_STR}/tables/orders/records",
            json=order_data
        )
        assert response.status_code == 200
    order_creation_time = time.time() - start_time
    assert order_creation_time < 1.0  # Should create 50 orders in under 1 second

    # Test join performance
    start_time = time.time()
    response = client.get(
        f"{settings.API_V1_STR}/tables/join",
        params={
            "table1": "users",
            "table2": "orders",
            "key": "user_id"
        }
    )
    join_time = time.time() - start_time
    assert join_time < 0.5  # Join should complete in under 0.5 seconds
    assert response.status_code == 200
    joined_data = response.json()
    assert len(joined_data) == 50  # Should have 50 joined records


def test_concurrent_read_performance(client: TestClient, setup_test_db, test_user):
    """Test performance of concurrent read operations."""
    start_time = time.time()
    for _ in range(1000):  # Simulate 1000 concurrent reads
        response = client.get(
            f"{settings.API_V1_STR}/tables/users/records/{test_user['id']}"
        )
        assert response.status_code == 200
    read_time = time.time() - start_time
    assert read_time < 2.0  # Should handle 1000 reads in under 2 seconds


def test_dump_performance(client: TestClient, setup_test_db):
    """Test performance of table dump operations."""
    # Create 100 test records first
    for _ in range(100):
        user_data = create_test_user()
        response = client.post(
            f"{settings.API_V1_STR}/tables/users/records",
            json=user_data
        )
        assert response.status_code == 200

    # Test dump performance
    start_time = time.time()
    response = client.get(f"{settings.API_V1_STR}/tables/users/dump")
    dump_time = time.time() - start_time
    assert dump_time < 0.5  # Should dump 100 records in under 0.5 seconds
    assert response.status_code == 200
    dumped_data = response.json()
    assert len(dumped_data) >= 100 
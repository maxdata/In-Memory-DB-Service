"""Tests for order-related operations in the in-memory database service."""

from fastapi.testclient import TestClient

from app.core.config import settings
from .test_helpers import create_test_order


def test_create_order(client: TestClient, setup_test_db, test_user):
    """Test creating a new order."""
    order_data = create_test_order(test_user["id"])
    response = client.post(
        f"{settings.API_V1_STR}/tables/orders/records",
        json=order_data
    )
    assert response.status_code == 200
    created_order = response.json()
    assert created_order["product"] == order_data["product"]
    assert created_order["quantity"] == order_data["quantity"]
    assert created_order["user_id"] == test_user["id"]
    assert "id" in created_order


def test_get_order(client: TestClient, setup_test_db, test_order):
    """Test retrieving an order by ID."""
    response = client.get(
        f"{settings.API_V1_STR}/tables/orders/records/{test_order['id']}"
    )
    assert response.status_code == 200
    order = response.json()
    assert order["product"] == test_order["product"]
    assert order["quantity"] == test_order["quantity"]
    assert order["user_id"] == test_order["user_id"]


def test_update_order(client: TestClient, setup_test_db, test_order):
    """Test updating an order's information."""
    update_data = {
        "product": "Updated Product",
        "quantity": 99
    }
    response = client.put(
        f"{settings.API_V1_STR}/tables/orders/records/{test_order['id']}",
        json=update_data
    )
    assert response.status_code == 200
    updated_order = response.json()
    assert updated_order["product"] == update_data["product"]
    assert updated_order["quantity"] == update_data["quantity"]
    assert updated_order["user_id"] == test_order["user_id"]


def test_delete_order(client: TestClient, setup_test_db, test_order):
    """Test deleting an order."""
    response = client.delete(
        f"{settings.API_V1_STR}/tables/orders/records/{test_order['id']}"
    )
    assert response.status_code == 200
    # Verify order is deleted
    get_response = client.get(
        f"{settings.API_V1_STR}/tables/orders/records/{test_order['id']}"
    )
    assert get_response.status_code == 404


def test_dump_orders(client: TestClient, setup_test_db, test_order):
    """Test dumping all orders from the database."""
    response = client.get(f"{settings.API_V1_STR}/tables/orders/dump")
    assert response.status_code == 200
    orders = response.json()
    assert isinstance(orders, list)
    assert len(orders) > 0
    assert any(order["id"] == test_order["id"] for order in orders)


def test_create_order_nonexistent_user(client: TestClient, setup_test_db):
    """Test attempting to create an order for a non-existent user."""
    order_data = create_test_order("nonexistent_user_id")
    response = client.post(
        f"{settings.API_V1_STR}/tables/orders/records",
        json=order_data
    )
    assert response.status_code == 400  # Bad request for non-existent user


def test_update_nonexistent_order(client: TestClient, setup_test_db):
    """Test attempting to update a non-existent order."""
    fake_id = "nonexistent_id"
    update_data = {"product": "New Product", "quantity": 5}
    response = client.put(
        f"{settings.API_V1_STR}/tables/orders/records/{fake_id}",
        json=update_data
    )
    assert response.status_code == 404  # Not found


def test_delete_nonexistent_order(client: TestClient, setup_test_db):
    """Test attempting to delete a non-existent order."""
    fake_id = "nonexistent_id"
    response = client.delete(
        f"{settings.API_V1_STR}/tables/orders/records/{fake_id}"
    )
    assert response.status_code == 404  # Not found


def test_join_users_orders(client: TestClient, setup_test_db, test_user, test_order):
    """Test joining users and orders tables."""
    response = client.get(
        f"{settings.API_V1_STR}/tables/join",
        params={
            "table1": "users",
            "table2": "orders",
            "key": "user_id"
        }
    )
    assert response.status_code == 200
    joined_data = response.json()
    assert isinstance(joined_data, list)
    assert len(joined_data) > 0
    
    # Verify join result contains expected data
    found_join = False
    for item in joined_data:
        if (item["users"]["id"] == test_user["id"] and 
            item["orders"]["id"] == test_order["id"]):
            found_join = True
            assert item["users"]["email"] == test_user["email"]
            assert item["orders"]["product"] == test_order["product"]
            assert item["orders"]["quantity"] == test_order["quantity"]
            break
    assert found_join, "Expected join result not found" 
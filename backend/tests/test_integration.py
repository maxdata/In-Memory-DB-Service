"""Integration tests for the in-memory database service."""

from fastapi.testclient import TestClient

from app.core.config import settings
from .test_helpers import create_test_user, create_test_order


def test_end_to_end_user_order_flow(client: TestClient, setup_test_db):
    """Test a complete workflow of user and order operations."""
    # 1. Create a user
    user_data = create_test_user()
    response = client.post(
        f"{settings.API_V1_STR}/tables/users/records",
        json=user_data
    )
    assert response.status_code == 200
    user = response.json()
    user_id = user["id"]

    # 2. Create multiple orders for the user
    orders = []
    for _ in range(3):
        order_data = create_test_order(user_id)
        response = client.post(
            f"{settings.API_V1_STR}/tables/orders/records",
            json=order_data
        )
        assert response.status_code == 200
        orders.append(response.json())

    # 3. Verify join results
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
    user_orders = [item for item in joined_data 
                  if item["users"]["id"] == user_id]
    assert len(user_orders) == 3

    # 4. Update an order
    update_data = {
        "product": "Updated Product",
        "quantity": 999
    }
    response = client.put(
        f"{settings.API_V1_STR}/tables/orders/records/{orders[0]['id']}",
        json=update_data
    )
    assert response.status_code == 200
    updated_order = response.json()
    assert updated_order["product"] == update_data["product"]
    assert updated_order["quantity"] == update_data["quantity"]

    # 5. Delete an order
    response = client.delete(
        f"{settings.API_V1_STR}/tables/orders/records/{orders[1]['id']}"
    )
    assert response.status_code == 200

    # 6. Verify final state
    response = client.get(f"{settings.API_V1_STR}/tables/orders/dump")
    assert response.status_code == 200
    final_orders = response.json()
    user_final_orders = [order for order in final_orders 
                        if order["user_id"] == user_id]
    assert len(user_final_orders) == 2

    # 7. Delete user and verify cascade effect
    response = client.delete(
        f"{settings.API_V1_STR}/tables/users/records/{user_id}"
    )
    assert response.status_code == 200

    # 8. Verify all user's orders are gone
    response = client.get(f"{settings.API_V1_STR}/tables/orders/dump")
    assert response.status_code == 200
    remaining_orders = response.json()
    user_remaining_orders = [order for order in remaining_orders 
                           if order["user_id"] == user_id]
    assert len(user_remaining_orders) == 0


def test_data_consistency_workflow(client: TestClient, setup_test_db):
    """Test data consistency across multiple operations."""
    # 1. Initial state
    response = client.get(f"{settings.API_V1_STR}/tables/users/dump")
    initial_user_count = len(response.json())

    # 2. Create users and verify count
    new_users = []
    for _ in range(5):
        user_data = create_test_user()
        response = client.post(
            f"{settings.API_V1_STR}/tables/users/records",
            json=user_data
        )
        assert response.status_code == 200
        new_users.append(response.json())

    response = client.get(f"{settings.API_V1_STR}/tables/users/dump")
    assert len(response.json()) == initial_user_count + 5

    # 3. Create orders and verify relationships
    for user in new_users:
        order_data = create_test_order(user["id"])
        response = client.post(
            f"{settings.API_V1_STR}/tables/orders/records",
            json=order_data
        )
        assert response.status_code == 200

    # 4. Verify join consistency
    response = client.get(
        f"{settings.API_V1_STR}/tables/join",
        params={
            "table1": "users",
            "table2": "orders",
            "key": "user_id"
        }
    )
    joined_data = response.json()
    new_user_joins = [item for item in joined_data 
                     if item["users"]["id"] in [u["id"] for u in new_users]]
    assert len(new_user_joins) == 5

    # 5. Delete users and verify cascade
    for user in new_users:
        response = client.delete(
            f"{settings.API_V1_STR}/tables/users/records/{user['id']}"
        )
        assert response.status_code == 200

    # 6. Verify final state matches initial state
    response = client.get(f"{settings.API_V1_STR}/tables/users/dump")
    assert len(response.json()) == initial_user_count

    response = client.get(f"{settings.API_V1_STR}/tables/orders/dump")
    remaining_orders = response.json()
    deleted_user_orders = [order for order in remaining_orders 
                         if order["user_id"] in [u["id"] for u in new_users]]
    assert len(deleted_user_orders) == 0 
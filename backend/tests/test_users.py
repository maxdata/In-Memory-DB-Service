"""Tests for user-related functionality in the in-memory database service."""


# Change to unit test pytest
# mock ?

# more edge cases: user_id avaialbe and not available

from fastapi.testclient import TestClient

from app.core.config import settings
from .test_helpers import create_test_user


def test_create_user(client: TestClient, setup_test_db):
    """Test creating a new user."""
    user_data = create_test_user()
    response = client.post(
        f"{settings.API_V1_STR}/tables/users/records",
        json=user_data
    )
    assert response.status_code == 200
    created_user = response.json()
    assert created_user["email"] == user_data["email"]
    assert "id" in created_user


def test_get_user(client: TestClient, setup_test_db, test_user):
    """Test retrieving a user by ID."""
    response = client.get(
        f"{settings.API_V1_STR}/tables/users/records/{test_user['id']}"
    )
    assert response.status_code == 200
    user = response.json()
    assert user["email"] == test_user["email"]


def test_update_user(client: TestClient, setup_test_db, test_user):
    """Test updating a user's information."""
    update_data = {"email": "updated@example.com"}
    response = client.put(
        f"{settings.API_V1_STR}/tables/users/records/{test_user['id']}",
        json=update_data
    )
    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user["email"] == update_data["email"]


def test_delete_user(client: TestClient, setup_test_db, test_user):
    """Test deleting a user."""
    response = client.delete(
        f"{settings.API_V1_STR}/tables/users/records/{test_user['id']}"
    )
    assert response.status_code == 200
    # Verify user is deleted
    get_response = client.get(
        f"{settings.API_V1_STR}/tables/users/records/{test_user['id']}"
    )
    assert get_response.status_code == 404


def test_dump_users(client: TestClient, setup_test_db, test_user):
    """Test dumping all users from the database."""
    response = client.get(f"{settings.API_V1_STR}/tables/users/dump")
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert len(users) > 0
    assert any(user["id"] == test_user["id"] for user in users)


def test_create_duplicate_user(client: TestClient, setup_test_db, test_user):
    """Test attempting to create a user with duplicate email."""
    duplicate_user = create_test_user(email=test_user["email"])
    response = client.post(
        f"{settings.API_V1_STR}/tables/users/records",
        json=duplicate_user
    )
    assert response.status_code == 400  # Bad request for duplicate email


def test_update_nonexistent_user(client: TestClient, setup_test_db):
    """Test attempting to update a non-existent user."""
    fake_id = "nonexistent_id"
    update_data = {"email": "new@example.com"}
    response = client.put(
        f"{settings.API_V1_STR}/tables/users/records/{fake_id}",
        json=update_data
    )
    assert response.status_code == 404  # Not found


def test_delete_nonexistent_user(client: TestClient, setup_test_db):
    """Test attempting to delete a non-existent user."""
    fake_id = "nonexistent_id"
    response = client.delete(
        f"{settings.API_V1_STR}/tables/users/records/{fake_id}"
    )
    assert response.status_code == 404  # Not found 
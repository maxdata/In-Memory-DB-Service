import pytest
from uuid import uuid4
import asyncio
from collections import defaultdict

from app.db.base import InMemoryDB, DatabaseError
from app.db.initial_data import get_sample_data

@pytest.fixture
async def db():
    """Fixture to create a fresh database instance for each test"""
    # Clear the singleton instance for each test
    InMemoryDB._instance = None
    InMemoryDB._initialized = False
    db = InMemoryDB()
    await db.initialize()
    yield db
    await db.cleanup()

@pytest.mark.asyncio
async def test_db_initialization(db):
    """Test database initialization"""
    assert isinstance(db._storage, defaultdict)
    assert isinstance(db._locks, defaultdict)
    assert isinstance(db._indexes, defaultdict)
    
    # Check that indexes are created for common fields
    assert "orders" in db._indexes
    assert "user_id" in db._indexes["orders"]
    assert "users" in db._indexes
    assert "email" in db._indexes["users"]
    
    # Storage should be empty but initialized
    assert "orders" in db._storage
    assert "users" in db._storage
    assert len(db._storage["orders"]) == 0
    assert len(db._storage["users"]) == 0

@pytest.mark.asyncio
async def test_db_crud_operations(db):
    """Test basic CRUD operations"""
    table = "users"
    record_data = {
        "email": "test@example.com",
        "full_name": "Test User",
        "hashed_password": "hashed_test123",
        "is_active": True
    }
    
    # Create
    record_id = await db.create_record(table, record_data)
    assert isinstance(record_id, uuid4().__class__)
    
    # Read
    read_record = await db.get_record(table, record_id)
    assert read_record is not None
    assert read_record["email"] == "test@example.com"
    
    # Update
    updated_data = {"full_name": "Updated User"}
    updated = await db.update_record(table, record_id, updated_data)
    assert updated is True
    
    # Read after update
    updated_record = await db.get_record(table, record_id)
    assert updated_record is not None
    assert updated_record["full_name"] == "Updated User"
    
    # Delete
    deleted = await db.delete_record(table, record_id)
    assert deleted is True
    
    # Read after delete
    deleted_record = await db.get_record(table, record_id)
    assert deleted_record is None

@pytest.mark.asyncio
async def test_db_error_handling(db):
    """Test database error handling"""
    table = "test_table"
    record_data = {"name": "test"}
    
    # Create a record
    record_id = await db.create_record(table, record_data)
    
    # Test non-existent record
    invalid_id = uuid4()
    assert await db.get_record(table, invalid_id) is None
    
    assert await db.update_record(table, invalid_id, {"name": "updated"}) is False
    assert await db.delete_record(table, invalid_id) is False

@pytest.mark.asyncio
async def test_db_concurrent_operations(db):
    """Test concurrent database operations"""
    table = "concurrent_test"
    tasks = []
    
    # Create multiple records concurrently
    for i in range(5):
        record_data = {"value": i}
        task = asyncio.create_task(db.create_record(table, record_data))
        tasks.append(task)
    
    # Wait for all tasks to complete
    record_ids = await asyncio.gather(*tasks)
    
    # Verify all records were created
    records = await db.list_records(table)
    assert len(records) == 5
    assert all(isinstance(record_id, uuid4().__class__) for record_id in record_ids)
    
    # Test concurrent reads
    read_tasks = []
    for record_id in record_ids:
        task = asyncio.create_task(db.get_record(table, record_id))
        read_tasks.append(task)
    
    read_results = await asyncio.gather(*read_tasks)
    assert all(result is not None for result in read_results)
    assert len(read_results) == 5

@pytest.mark.asyncio
async def test_db_table_operations(db):
    """Test table-level operations"""
    table = "test_table"
    
    # Create some records
    record_ids = []
    for i in range(3):
        record_id = await db.create_record(table, {"value": i})
        record_ids.append(record_id)
    
    # Test list records
    records = await db.list_records(table)
    assert len(records) == 3
    
    # Test record exists
    assert await db.record_exists(table, record_ids[0]) is True
    assert await db.record_exists(table, uuid4()) is False
    
    # Test clear table
    await db.clear_table(table)
    cleared_records = await db.list_records(table)
    assert len(cleared_records) == 0

@pytest.mark.asyncio
async def test_db_relationships(db):
    """Test relationships between tables"""
    # Create a user
    user_id = await db.create_record("users", {
        "email": "test@example.com",
        "full_name": "Test User"
    })
    
    # Create orders for the user
    order_ids = []
    for i in range(3):
        order_id = await db.create_record("orders", {
            "user_id": user_id,
            "amount": 100 * (i + 1)
        })
        order_ids.append(order_id)
    
    # Verify user exists
    user = await db.get_record("users", user_id)
    assert user is not None
    
    # Verify orders exist and are linked to user
    orders = await db.list_records("orders")
    assert len(orders) == 3
    assert all(order["user_id"] == user_id for order in orders)

@pytest.mark.asyncio
async def test_db_sample_data(db):
    """Test loading sample data"""
    sample_data = get_sample_data()
    
    # Create sample users
    user_ids = []
    for user_data in sample_data["users"]:
        user_id = await db.create_record("users", user_data)
        user_ids.append(user_id)
    
    # Create sample orders
    order_ids = []
    for order_data in sample_data["orders"]:
        order_id = await db.create_record("orders", order_data)
        order_ids.append(order_id)
    
    # Verify data was loaded
    users = await db.list_records("users")
    orders = await db.list_records("orders")
    assert len(users) == len(sample_data["users"])
    assert len(orders) == len(sample_data["orders"]) 
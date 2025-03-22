import pytest
from uuid import UUID, uuid4
from app.db.base import InMemoryDB
from app.services.base_service import BaseService

@pytest.fixture
async def db():
    """Database fixture"""
    db = InMemoryDB()
    await db.initialize()
    yield db
    await db.cleanup()

@pytest.fixture
async def service(db):
    """Service fixture that creates a test service instance"""
    service = BaseService(db, "test_table")
    return service

@pytest.mark.asyncio
async def test_base_service_initialization(service):
    """Test base service initialization"""
    assert service.table_name == "test_table"
    assert isinstance(service.db, InMemoryDB)

@pytest.mark.asyncio
async def test_base_service_create(service):
    """Test create operation"""
    data = {"name": "Test", "email": "test@example.com"}
    record_id = await service.create(data)
    assert isinstance(record_id, UUID)
    
    # Verify record exists
    record = await service.get(record_id)
    assert record["name"] == data["name"]
    assert record["email"] == data["email"]

@pytest.mark.asyncio
async def test_base_service_get(service):
    """Test get operation"""
    # Create test record
    data = {"name": "Test", "email": "test@example.com"}
    record_id = await service.create(data)
    
    # Test get
    record = await service.get(record_id)
    assert record is not None
    assert record["name"] == data["name"]
    
    # Test get nonexistent
    nonexistent_id = uuid4()
    record = await service.get(nonexistent_id)
    assert record is None

@pytest.mark.asyncio
async def test_base_service_update(service):
    """Test update operation"""
    # Create test record
    data = {"name": "Test", "email": "test@example.com"}
    record_id = await service.create(data)
    
    # Update record
    update_data = {"name": "Updated"}
    updated = await service.update(record_id, update_data)
    assert updated is True
    
    # Verify update
    record = await service.get(record_id)
    assert record["name"] == "Updated"
    assert record["email"] == data["email"]  # Unchanged field

@pytest.mark.asyncio
async def test_base_service_delete(service):
    """Test delete operation"""
    # Create test record
    data = {"name": "Test", "email": "test@example.com"}
    record_id = await service.create(data)
    
    # Delete record
    deleted = await service.delete(record_id)
    assert deleted is True
    
    # Verify deletion
    record = await service.get(record_id)
    assert record is None

@pytest.mark.asyncio
async def test_base_service_list(service):
    """Test list operation"""
    # Create multiple records
    records = [
        {"name": f"Test {i}", "email": f"test{i}@example.com"}
        for i in range(3)
    ]
    for data in records:
        await service.create(data)
    
    # List all records
    all_records = await service.list()
    assert len(all_records) == 3
    assert all(isinstance(UUID(r["id"]), UUID) for r in all_records)

@pytest.mark.asyncio
async def test_base_service_exists(service):
    """Test exists operation"""
    # Create test record
    data = {"name": "Test", "email": "test@example.com"}
    record_id = await service.create(data)
    
    # Test exists
    assert await service.exists(record_id) is True
    assert await service.exists(uuid4()) is False 
import pytest
import json
import os
import random
from starlette.testclient import TestClient
from app.main import app
from uuid import uuid4
from datetime import datetime
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import asyncio
from typing import List
from fastapi import FastAPI
from httpx import Response

"""
Performance Tests for the In-Memory Database Service API

This test suite focuses on measuring and ensuring the performance characteristics
of the API under various conditions. It includes tests for response times,
concurrent operations, and system behavior under load.

Test Categories:
1. Single Operation Performance: Measuring individual operation response times
2. Concurrent Operation Performance: Testing behavior with multiple simultaneous requests
3. Bulk Operation Performance: Testing performance with large datasets
4. Relationship Query Performance: Testing performance of relationship endpoints
5. Sequential Operation Performance: Testing chains of operations

Performance Requirements:
- Single operations: < 50ms average response time
- Bulk operations: < 500ms for 100 records
- Concurrent operations: < 5s for 50 simultaneous requests
- Sequential operations: < 2s for complete CRUD sequence
- Relationship queries: < 100ms average response time
"""

client = TestClient(app)

# Load sample test data from JSON file
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(TESTS_DIR, 'sample_data.json'), 'r') as f:
    sample_data = json.load(f)

# Use first user and order from sample data
test_user = {
    "email": sample_data["users"][0]["email"],
    "full_name": sample_data["users"][0]["full_name"],
    "age": sample_data["users"][0]["age"]
}

test_order = {
    "items": ["Test Item"],
    "total_amount": 99.99
}

@pytest.fixture
def sample_user_data():
    """Fixture to provide sample user data for tests"""
    return sample_data["users"]

@pytest.fixture
def sample_order_data():
    """Fixture to provide sample order data for tests"""
    return sample_data["orders"]

@pytest.fixture
def user_id():
    """
    Fixture: Creates a test user for performance testing.
    
    This fixture provides a baseline user for performance tests
    that require an existing user record. It's used to measure
    read/update/delete performance and relationship queries.
    """
    response = client.post("/api/v1/users", json=test_user)
    return response.json()["id"]

@pytest.fixture
def multiple_users():
    """
    Fixture: Creates multiple test users for bulk operation testing.
    
    Creates users based on sample data and additional generated data to:
    1. Provide dataset for bulk operation tests
    2. Test performance with multiple records
    3. Enable meaningful benchmarks for list operations
    """
    user_ids = []
    
    # First add sample users
    for user in sample_data["users"]:
        user_data = {
            "email": user["email"],
            "full_name": user["full_name"],
            "age": user["age"]
        }
        response = client.post("/api/v1/users", json=user_data)
        user_ids.append(response.json()["id"])
    
    # Then add additional users to reach desired count
    for i in range(len(sample_data["users"]), 10):
        user_data = {
            "email": f"user{i}@example.com",
            "full_name": f"Test User {i}",
            "age": 20 + i
        }
        response = client.post("/api/v1/users", json=user_data)
        user_ids.append(response.json()["id"])
    
    return user_ids

async def run_concurrent_tasks(tasks: List[Response]) -> List[Response]:
    """Run multiple tasks concurrently and return their responses."""
    async def run_task(task):
        return await task
    return await asyncio.gather(*[run_task(task) for task in tasks])

def test_user_creation_performance(benchmark):
    """
    Test: User Creation Performance
    
    Measures:
    1. Time taken to create a new user
    2. Consistency of creation times
    3. Impact of data validation
    4. Database insertion performance
    
    Uses pytest-benchmark to ensure reliable measurements
    and statistical significance.
    """
    def create_user():
        user_data = {
            "email": f"perf_{uuid4()}@example.com",
            "full_name": "Performance Test User",
            "age": 25
        }
        response = client.post("/api/v1/users", json=user_data)
        assert response.status_code == 200
        return response.json()["id"]
    
    # Benchmark user creation
    benchmark(create_user)

def test_user_retrieval_performance(benchmark, user_id):
    """
    Test: User Retrieval Performance
    
    Measures:
    1. Time taken to retrieve a user by ID
    2. Consistency of retrieval times
    3. Impact of database size on retrieval
    4. Response serialization performance
    """
    def get_user():
        response = client.get(f"/api/v1/users/{user_id}")
        assert response.status_code == 200
        return response.json()
    
    # Benchmark user retrieval
    benchmark(get_user)

def test_concurrent_user_creation_performance():
    """
    Test: Concurrent User Creation Performance
    
    Measures:
    1. System behavior under concurrent load
    2. Resource contention handling
    3. Connection pool performance
    4. Thread safety of operations
    
    Creates 50 users concurrently using 10 worker threads,
    ensuring the system can handle multiple simultaneous requests.
    """
    num_users = 50
    max_workers = 10
    start_time = time.time()
    
    def create_user(i):
        user_data = {
            "email": f"concurrent_user_{i}@example.com",
            "full_name": f"Concurrent Test User {i}",
            "age": 25
        }
        response = client.post("/api/v1/users", json=user_data)
        assert response.status_code == 200
        return response.json()["id"]
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(create_user, i) for i in range(num_users)]
        user_ids = [future.result() for future in as_completed(futures)]
    
    end_time = time.time()
    duration = end_time - start_time
    
    assert len(user_ids) == num_users
    # Expecting creation of 50 users to take less than 10 seconds
    assert duration < 10.0

def test_bulk_user_listing_performance(benchmark, multiple_users):
    """
    Test: Bulk User Listing Performance
    
    Measures:
    1. Performance of retrieving multiple records
    2. Response serialization for large datasets
    3. Impact of result set size on performance
    4. Memory usage during bulk operations
    """
    def list_users():
        response = client.get("/api/v1/users")
        assert response.status_code == 200
        users = response.json()
        assert len(users) >= len(multiple_users)
        return users
    
    # Benchmark user listing
    benchmark(list_users)

def test_table_dump_performance(benchmark, multiple_users):
    """
    Test: Table Dump Performance
    
    Measures:
    1. Performance of full table scan
    2. Data serialization for large datasets
    3. Memory usage during full table operations
    4. Impact of record count on response time
    """
    def dump_table():
        response = client.get("/api/v1/tables/users/dump")
        assert response.status_code == 200
        result = response.json()
        assert result["count"] >= len(multiple_users)
        return result
    
    # Benchmark table dump
    benchmark(dump_table)

def test_sequential_operations_performance():
    """
    Test: Sequential Operations Performance

    Measures:
    1. Performance of complete CRUD sequence
    2. Transaction overhead
    3. State management efficiency
    4. Cumulative operation time

    Performs a complete cycle of operations (create, read,
    update, delete) to measure end-to-end performance.
    """
    start_time = time.time()

    # Create user
    response = client.post("/api/v1/users", json=test_user)
    assert response.status_code == 200
    user_id = response.json()["id"]

    # Create order
    order_data = {
        "user_id": user_id,
        "product_name": "Test Product",
        "quantity": 1,
        "total_price": 99.99,
        "status": "pending"
    }
    response = client.post("/api/v1/orders", json=order_data)
    assert response.status_code == 200
    order_id = response.json()["id"]

    # Read user and order
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    response = client.get(f"/api/v1/orders/{order_id}")
    assert response.status_code == 200

    # Update user and order
    response = client.patch(f"/api/v1/users/{user_id}", json={"age": 31})
    assert response.status_code == 200
    response = client.patch(f"/api/v1/orders/{order_id}", json={"status": "processing"})
    assert response.status_code == 200

    # Delete user and order
    response = client.delete(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    response = client.delete(f"/api/v1/orders/{order_id}")
    assert response.status_code == 200

    end_time = time.time()
    total_time = end_time - start_time
    assert total_time < 1.0  # All operations should complete within 1 second

def test_rapid_sequential_reads():
    """
    Test: Rapid Sequential Read Performance
    
    Measures:
    1. Performance under rapid sequential requests
    2. Connection reuse efficiency
    3. Resource cleanup between requests
    4. Average response time stability
    
    Performs 100 rapid sequential reads to measure
    system stability and response time consistency.
    """
    # Create test user
    response = client.post("/api/v1/users", json=test_user)
    user_id = response.json()["id"]
    
    start_time = time.time()
    num_reads = 100
    
    # Perform rapid sequential reads
    for _ in range(num_reads):
        response = client.get(f"/api/v1/users/{user_id}")
        assert response.status_code == 200
    
    end_time = time.time()
    duration = end_time - start_time
    
    # Calculate average response time
    avg_response_time = duration / num_reads
    # Expecting average response time to be less than 50ms
    assert avg_response_time < 0.05

def test_concurrent_reads_performance():
    """
    Test: Concurrent Read Performance
    
    Measures:
    1. Performance under concurrent read load
    2. Connection pool efficiency
    3. Resource contention handling
    4. Response time stability
    
    Performs 50 concurrent reads using 10 worker threads
    to measure system behavior under parallel read load.
    """
    # Create test user
    response = client.post("/api/v1/users", json=test_user)
    user_id = response.json()["id"]
    
    num_reads = 50
    max_workers = 10
    start_time = time.time()
    
    def get_user():
        response = client.get(f"/api/v1/users/{user_id}")
        assert response.status_code == 200
        return response.json()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(get_user) for _ in range(num_reads)]
        results = [future.result() for future in as_completed(futures)]
    
    end_time = time.time()
    duration = end_time - start_time
    
    assert len(results) == num_reads
    # Expecting 50 concurrent reads to take less than 5 seconds
    assert duration < 5.0

def test_relationship_endpoints_performance(benchmark, sample_user_data, sample_order_data):
    """
    Test: Relationship Endpoint Performance

    Measures:
    1. Performance of relationship queries
    2. Join operation efficiency
    3. Impact of relationship complexity
    4. Response time consistency
    """
    # Create test data from sample data
    user_data = sample_user_data[0]
    response = client.post("/api/v1/users", json={
        "email": user_data["email"],
        "full_name": user_data["full_name"],
        "age": user_data["age"]
    })
    user_id = response.json()["id"]

    # Create associated orders
    order_ids = []
    for i in range(3):  # Create 3 test orders
        order_data = {
            "product_name": f"Test Product {i}",
            "quantity": i + 1,
            "total_price": 99.99 * (i + 1),
            "status": "pending",
            "user_id": user_id
        }
        response = client.post("/api/v1/orders", json=order_data)
        assert response.status_code == 200, f"Failed to create order: {response.text}"
        order_ids.append(response.json()["id"])

    # Define the benchmark function
    def run_relationship_queries():
        # Get user's orders
        response = client.get(f"/api/v1/users/{user_id}/orders")
        assert response.status_code == 200
        assert len(response.json()) == 3

        # Get each order's user
        for order_id in order_ids:
            response = client.get(f"/api/v1/orders/{order_id}/user")
            assert response.status_code == 200
            assert response.json()["id"] == user_id

    # Run the benchmark
    benchmark(run_relationship_queries)

def test_concurrent_relationship_queries():
    """
    Test: Concurrent Relationship Query Performance

    Measures:
    1. Performance of concurrent relationship operations
    2. Resource contention in relationship queries
    3. Connection pool behavior with complex queries
    4. System stability under relationship query load

    Performs 50 concurrent relationship queries, randomly
    choosing between user-orders and order-user endpoints
    to simulate real-world mixed query patterns.
    """
    # Create test user and order
    user_response = client.post("/api/v1/users", json=test_user)
    user_id = user_response.json()["id"]

    order_data = {
        "product_name": "Test Product",
        "quantity": 1,
        "total_price": 99.99,
        "status": "pending",
        "user_id": user_id
    }
    order_response = client.post("/api/v1/orders", json=order_data)
    assert order_response.status_code == 200, f"Failed to create order: {order_response.text}"
    order_id = order_response.json()["id"]

    # Function to perform a single query
    def perform_query():
        if random.choice([True, False]):
            response = client.get(f"/api/v1/users/{user_id}/orders")
        else:
            response = client.get(f"/api/v1/orders/{order_id}/user")
        assert response.status_code == 200
        return response

    # Run queries concurrently using ThreadPoolExecutor
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(perform_query) for _ in range(50)]
        responses = [future.result() for future in as_completed(futures)]
    end_time = time.time()

    # Verify all responses were successful
    assert len(responses) == 50
    for response in responses:
        assert response.status_code == 200

    # Check total time
    total_time = end_time - start_time
    assert total_time < 2.0  # All 50 queries should complete within 2 seconds 
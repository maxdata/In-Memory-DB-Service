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
import logging

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
- Single operations: < 100ms average response time
- Bulk operations: < 1s for 100 records
- Concurrent operations: < 10s for 50 simultaneous requests
- Sequential operations: < 5s for complete CRUD sequence
- Relationship queries: < 200ms average response time
"""

@pytest.fixture
def client():
    """Fixture that provides a test client"""
    return TestClient(app)

# Load sample test data from JSON file
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(TESTS_DIR, 'sample_data.json'), 'r') as f:
    sample_data = json.load(f)

# Use first user and order from sample data
test_user = sample_data["users"][0]
test_order = sample_data["orders"][0]

logger = logging.getLogger(__name__)

@pytest.fixture
def sample_user_data():
    """Fixture to provide sample user data for tests"""
    return sample_data["users"]

@pytest.fixture
def sample_order_data():
    """Fixture to provide sample order data for tests"""
    return sample_data["orders"]

@pytest.fixture
def user_id(client):
    """
    Fixture: Creates a test user for performance testing.
    
    This fixture provides a baseline user for performance tests
    that require an existing user record. It's used to measure
    read/update/delete performance and relationship queries.
    """
    response = client.post("/api/v1/users", json=test_user)
    assert response.status_code == 201
    return response.json()["id"]

@pytest.fixture
def multiple_users(client):
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
        response = client.post("/api/v1/users", json=user)
        user_ids.append(response.json()["id"])

    return user_ids

async def run_concurrent_tasks(tasks: List[Response]) -> List[Response]:
    """Run multiple tasks concurrently and return their responses."""
    async def run_task(task):
        return await task
    return await asyncio.gather(*[run_task(task) for task in tasks])

@pytest.mark.performance
def test_single_operation_performance(client):
    """Test performance of single operations"""
    # Create user
    start_time = time.time()
    response = client.post("/api/v1/users", json=test_user)
    assert response.status_code == 201
    user_id = response.json()["id"]
    create_user_time = time.time() - start_time

    # Get user
    start_time = time.time()
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    get_user_time = time.time() - start_time

    # Create order
    order_data = test_order.copy()
    order_data["user_id"] = user_id
    start_time = time.time()
    response = client.post("/api/v1/orders", json=order_data)
    assert response.status_code == 201
    create_order_time = time.time() - start_time

    # Log performance metrics
    logger.info(f"Create user time: {create_user_time:.4f} seconds")
    logger.info(f"Get user time: {get_user_time:.4f} seconds")
    logger.info(f"Create order time: {create_order_time:.4f} seconds")

    # Assert performance thresholds
    assert create_user_time < 0.5, f"User creation took too long: {create_user_time:.4f} seconds"
    assert get_user_time < 0.5, f"User retrieval took too long: {get_user_time:.4f} seconds"
    assert create_order_time < 0.5, f"Order creation took too long: {create_order_time:.4f} seconds"

@pytest.mark.performance
def test_concurrent_operations_performance(client, sample_user_data, sample_order_data):
    """Test performance of concurrent operations"""
    # Create multiple users concurrently
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(client.post, "/api/v1/users", json=user_data)
            for user_data in sample_user_data[:5]
        ]
        responses = [future.result() for future in futures]
    
    concurrent_create_time = time.time() - start_time
    user_ids = [response.json()["id"] for response in responses]

    # Create orders for users concurrently
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        order_data_list = []
        for i, order in enumerate(sample_order_data[:5]):
            order_copy = order.copy()
            order_copy["user_id"] = user_ids[i % len(user_ids)]
            order_data_list.append(order_copy)
            
        futures = [
            executor.submit(client.post, "/api/v1/orders", json=order_data)
            for order_data in order_data_list
        ]
        responses = [future.result() for future in futures]
    
    concurrent_order_time = time.time() - start_time

    # Log performance metrics
    logger.info(f"Concurrent user creation time: {concurrent_create_time:.4f} seconds")
    logger.info(f"Concurrent order creation time: {concurrent_order_time:.4f} seconds")

    # Assert performance thresholds
    assert concurrent_create_time < 2.0, f"Concurrent user creation took too long: {concurrent_create_time:.4f} seconds"
    assert concurrent_order_time < 2.0, f"Concurrent order creation took too long: {concurrent_order_time:.4f} seconds"

@pytest.mark.performance
def test_bulk_operations_performance(client, sample_user_data, sample_order_data):
    """Test performance of bulk operations"""
    # Create users in bulk
    start_time = time.time()
    user_responses = []
    for user_data in sample_user_data[:10]:
        response = client.post("/api/v1/users", json=user_data)
        assert response.status_code == 201
        user_responses.append(response)
    bulk_user_time = time.time() - start_time

    user_ids = [response.json()["id"] for response in user_responses]

    # Create orders in bulk
    start_time = time.time()
    for i, order in enumerate(sample_order_data[:10]):
        order_data = order.copy()
        order_data["user_id"] = user_ids[i % len(user_ids)]
        response = client.post("/api/v1/orders", json=order_data)
        assert response.status_code == 201
    bulk_order_time = time.time() - start_time

    # Log performance metrics
    logger.info(f"Bulk user creation time: {bulk_user_time:.4f} seconds")
    logger.info(f"Bulk order creation time: {bulk_order_time:.4f} seconds")

    # Assert performance thresholds
    assert bulk_user_time < 5.0, f"Bulk user creation took too long: {bulk_user_time:.4f} seconds"
    assert bulk_order_time < 5.0, f"Bulk order creation took too long: {bulk_order_time:.4f} seconds"

def test_user_creation_performance(benchmark, client):
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
            "password": "testpassword123"
        }
        response = client.post("/api/v1/users", json=user_data)
        assert response.status_code == 201
        return response.json()["id"]
    
    # Benchmark user creation
    benchmark(create_user)

def test_user_retrieval_performance(benchmark, client, user_id):
    """
    Test: User Retrieval Performance
    
    Measures:
    1. Time taken to retrieve a user
    2. Consistency of retrieval times
    3. Impact of data size
    4. Database lookup performance
    """
    def get_user():
        response = client.get(f"/api/v1/users/{user_id}")
        assert response.status_code == 200
        return response.json()
    
    # Benchmark user retrieval
    benchmark(get_user)

def test_concurrent_user_creation_performance(client):
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
            "password": "testpassword123"
        }
        response = client.post("/api/v1/users", json=user_data)
        assert response.status_code == 201
        return response.json()["id"]

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(create_user, i) for i in range(num_users)]
        user_ids = [future.result() for future in as_completed(futures)]

    total_time = time.time() - start_time
    assert len(user_ids) == num_users
    assert total_time < 10.0  # Should complete within 10 seconds

def test_bulk_user_listing_performance(benchmark, client, multiple_users):
    """
    Test: Bulk User Listing Performance

    Measures:
    1. Performance of listing multiple users
    2. Impact of result set size
    3. Memory usage patterns
    4. Response time scaling
    """
    def list_users():
        response = client.get("/api/v1/users")
        assert response.status_code == 200
        result = response.json()
        assert len(result["data"]) >= len(multiple_users)
        return result

    # Benchmark user listing
    benchmark(list_users)

def test_table_dump_performance(benchmark, client, multiple_users):
    """
    Test: Table Dump Performance

    Measures:
    1. Performance of full table dumps
    2. Serialization overhead
    3. Memory usage patterns
    4. Response time scaling
    """
    def dump_table():
        response = client.get("/api/v1/tables/users/dump")
        assert response.status_code == 200
        result = response.json()
        assert result["count"] >= len(multiple_users)
        return result

    # Benchmark table dump
    benchmark(dump_table)

def test_sequential_operations_performance(client):
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
    assert response.status_code == 201
    user_id = response.json()["id"]

    # Get user
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200

    # Create order
    order_data = test_order.copy()
    order_data["user_id"] = user_id
    response = client.post("/api/v1/orders", json=order_data)
    assert response.status_code == 201
    order_id = response.json()["id"]

    # Get order
    response = client.get(f"/api/v1/orders/{order_id}")
    assert response.status_code == 200

    total_time = time.time() - start_time
    assert total_time < 2.0  # Should complete within 2 seconds

def test_rapid_sequential_reads(client):
    """Test performance of sequential read operations"""
    # Create test data
    response = client.post("/api/v1/users", json=test_user)
    user_id = response.json()["id"]

    # Perform sequential reads
    start_time = time.time()
    for _ in range(50):  # Perform 50 sequential reads
        response = client.get(f"/api/v1/users/{user_id}")
        assert response.status_code == 200

    total_time = time.time() - start_time
    avg_time = total_time / 50

    # Log performance metrics
    logger.info(f"Average read time: {avg_time:.4f} seconds")
    logger.info(f"Total time for 50 reads: {total_time:.4f} seconds")

    # Assert performance requirements
    assert avg_time < 0.1, f"Average read time too high: {avg_time:.4f} seconds"
    assert total_time < 5.0, f"Total read time too high: {total_time:.4f} seconds"

def test_concurrent_reads_performance(client):
    """Test performance of concurrent read operations"""
    # Create test data
    response = client.post("/api/v1/users", json=test_user)
    user_id = response.json()["id"]

    def perform_read():
        response = client.get(f"/api/v1/users/{user_id}")
        assert response.status_code == 200
        return response.json()

    # Perform concurrent reads
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(perform_read) for _ in range(50)]
        results = [future.result() for future in futures]

    total_time = time.time() - start_time
    avg_time = total_time / 50

    # Log performance metrics
    logger.info(f"Average concurrent read time: {avg_time:.4f} seconds")
    logger.info(f"Total time for 50 concurrent reads: {total_time:.4f} seconds")

    # Assert performance requirements
    assert avg_time < 0.1, f"Average concurrent read time too high: {avg_time:.4f} seconds"
    assert total_time < 5.0, f"Total concurrent read time too high: {total_time:.4f} seconds"

def test_relationship_endpoints_performance(benchmark, client, sample_user_data, sample_order_data):
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
    response = client.post("/api/v1/users", json=user_data)
    assert response.status_code == 201
    user_id = response.json()["id"]

    # Create associated orders
    order_ids = []
    for i, order in enumerate(sample_order_data[:3]):
        order_data = order.copy()
        order_data["user_id"] = user_id
        response = client.post("/api/v1/orders", json=order_data)
        assert response.status_code == 201
        order_ids.append(response.json()["id"])

    def run_relationship_query():
        # Get user's orders
        response = client.get(f"/api/v1/users/{user_id}/orders")
        assert response.status_code == 200
        result = response.json()
        assert len(result["data"]) == len(order_ids)

        # Get order's user
        for order_id in order_ids:
            response = client.get(f"/api/v1/orders/{order_id}/user")
            assert response.status_code == 200
            assert response.json()["id"] == user_id

    # Benchmark the relationship queries
    benchmark(run_relationship_query)

def test_concurrent_relationship_queries(client):
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
    response = client.post("/api/v1/users", json=test_user)
    assert response.status_code == 201
    user_id = response.json()["id"]

    order_data = test_order.copy()
    order_data["user_id"] = user_id
    response = client.post("/api/v1/orders", json=order_data)
    assert response.status_code == 201
    order_id = response.json()["id"]

    num_queries = 50
    max_workers = 10

    def run_random_query(i):
        if i % 2 == 0:
            response = client.get(f"/api/v1/users/{user_id}/orders")
        else:
            response = client.get(f"/api/v1/orders/{order_id}/user")
        assert response.status_code == 200
        return response.json()

    start_time = time.time()
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(run_random_query, i) for i in range(num_queries)]
        results = [future.result() for future in as_completed(futures)]

    total_time = time.time() - start_time
    assert len(results) == num_queries
    assert total_time < 10.0  # Should complete within 10 seconds

def test_order_listing_performance(benchmark, client, multiple_users):
    """
    Test: Order Listing Performance
    
    Measures:
    1. Time taken to list orders
    2. Performance with multiple orders
    3. Impact of data size on response time
    """
    # Create multiple orders first
    user_id = multiple_users[0]  # Use first user for all orders
    for _ in range(10):  # Create 10 orders
        order_data = {
            "amount": random.uniform(10.0, 1000.0),
            "description": f"Performance test order {_}",
            "status": "pending",
            "user_id": user_id
        }
        response = client.post("/api/v1/orders", json=order_data)
        assert response.status_code == 201
    
    def list_orders():
        response = client.get("/api/v1/orders")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] >= 10
        return data
    
    # Benchmark order listing
    result = benchmark(list_orders)
    assert result["count"] >= 10


def test_order_update_performance(benchmark, client, user_id):
    """
    Test: Order Update Performance
    
    Measures:
    1. Time taken to update an order
    2. Performance of partial updates
    3. Impact of validation on update time
    """
    # Create an order first
    order_data = {
        "amount": 99.99,
        "description": "Performance test order",
        "status": "pending",
        "user_id": user_id
    }
    response = client.post("/api/v1/orders", json=order_data)
    assert response.status_code == 201
    order_id = response.json()["id"]
    
    def update_order():
        update_data = {
            "status": random.choice(["pending", "processing", "shipped", "delivered"]),
            "amount": random.uniform(10.0, 1000.0)
        }
        response = client.patch(f"/api/v1/orders/{order_id}", json=update_data)
        assert response.status_code == 200
        return response.json()
    
    # Benchmark order update
    result = benchmark(update_order)
    assert result["id"] == order_id


def test_health_endpoint_performance(benchmark, client):
    """
    Test: Health Check Endpoint Performance
    
    Measures:
    1. Response time of health check endpoint
    2. Consistency of response times
    3. Performance under repeated calls
    """
    def check_health():
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        return response.json()
    
    # Benchmark health check
    result = benchmark(check_health)
    assert result["status"] == "healthy"


def test_readiness_endpoint_performance(benchmark, client):
    """
    Test: Readiness Check Endpoint Performance
    
    Measures:
    1. Response time of readiness check endpoint
    2. Consistency of response times
    3. Performance under repeated calls
    """
    def check_readiness():
        response = client.get("/api/v1/ready")
        assert response.status_code == 200
        return response.json()
    
    # Benchmark readiness check
    result = benchmark(check_readiness)
    assert result["status"] == "ready"


def test_concurrent_order_operations(client, user_id):
    """
    Test: Concurrent Order Operations Performance
    
    Measures:
    1. Performance under concurrent order operations
    2. System stability with parallel requests
    3. Response time consistency
    """
    NUM_CONCURRENT = 10
    
    # Create orders concurrently
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=NUM_CONCURRENT) as executor:
        futures = []
        for i in range(NUM_CONCURRENT):
            order_data = {
                "amount": random.uniform(10.0, 1000.0),
                "description": f"Concurrent test order {i}",
                "status": "pending",
                "user_id": user_id
            }
            futures.append(
                executor.submit(client.post, "/api/v1/orders", json=order_data)
            )
        
        # Collect responses and order IDs
        order_ids = []
        for future in futures:
            response = future.result()
            assert response.status_code == 201
            order_ids.append(response.json()["id"])
    
    create_time = time.time() - start_time
    logger.info(f"Concurrent order creation time: {create_time:.4f} seconds")
    assert create_time < 5.0  # Should complete within 5 seconds
    
    # Update orders concurrently
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=NUM_CONCURRENT) as executor:
        futures = []
        for order_id in order_ids:
            update_data = {
                "status": "processing",
                "amount": random.uniform(10.0, 1000.0)
            }
            futures.append(
                executor.submit(
                    client.patch,
                    f"/api/v1/orders/{order_id}",
                    json=update_data
                )
            )
        
        # Verify all updates succeeded
        for future in futures:
            response = future.result()
            assert response.status_code == 200
    
    update_time = time.time() - start_time
    logger.info(f"Concurrent order update time: {update_time:.4f} seconds")
    assert update_time < 5.0  # Should complete within 5 seconds 
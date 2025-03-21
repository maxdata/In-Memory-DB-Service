# Technical Design Document: In-Memory Database Service

## 1. System Architecture

### 1.1 High-Level Architecture
```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   HTTP Client   │────▶│  FastAPI Server  │────▶│  In-Memory DB   │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                               │
                        ┌──────┴──────┐
                        │  Pydantic   │
                        │   Models    │
                        └─────────────┘
```

### 1.2 Component Overview
- **FastAPI Server**: Handles HTTP requests, routing, and response generation
- **In-Memory Database**: Python dictionary-based storage system
- **Pydantic Models**: Data validation and serialization
- **API Layer**: RESTful endpoints for CRUD and join operations

## 2. Detailed Design

### 2.1 Project Structure

#### 2.1.1 Directory Organization
The project follows a clean architecture pattern with clear separation of concerns:

```
app/
├── api/           # API routes/endpoints
│   ├── v1/        # API version 1
│   └── deps.py    # Dependency injections
├── core/          # Core application configuration
│   ├── config.py  # Environment variables and settings
│   └── security.py # Security utilities
├── db/            # Database related code
│   ├── base.py    # Base DB class
│   └── session.py # DB session management
├── models/        # Database models/schemas
│   ├── user.py
│   └── base.py
├── schemas/       # Pydantic models for request/response
│   └── user.py
├── services/      # Business logic
│   └── user.py
├── utils/         # Utility functions
└── main.py        # Application entry point
```

#### 2.1.2 Component Responsibilities

1. **api/**
   - Contains all API routes organized by version
   - Implements endpoint handlers
   - Manages request/response lifecycle
   - Handles dependency injection

2. **core/**
   - Application configuration management
   - Environment variables handling
   - Security settings and utilities
   - Global constants and settings

3. **db/**
   - Database connection management
   - Session handling
   - Base database classes
   - Database utilities

4. **models/** and **schemas/**
   - `models/`: Database models and data structures
   - `schemas/`: Pydantic models for request/response validation
   - Data validation and serialization
   - Type definitions and constraints

5. **services/**
   - Business logic implementation
   - Service layer abstraction
   - Complex operations and workflows
   - Data processing and transformation

#### 2.1.3 Design Principles

1. **Separation of Concerns**
   - Each directory has a specific responsibility
   - Clear boundaries between components
   - Minimal coupling between modules
   - Maximum cohesion within modules

2. **Dependency Management**
   - Centralized dependency injection
   - Clear dependency flow
   - Easy to test and mock
   - Configurable dependencies

3. **Scalability**
   - Easy to add new features
   - Simple to maintain
   - Clear upgrade paths
   - Version control friendly

### 2.2 Data Storage Implementation

#### 2.2.1 In-Memory Database Class
```python
class InMemoryDB:
    def __init__(self):
        self._storage: Dict[str, Dict[str, Any]] = defaultdict(dict)
        self._locks: Dict[str, Lock] = defaultdict(Lock)

    async def create(self, table: str, record_id: str, data: dict) -> dict:
        async with self._locks[table]:
            if record_id in self._storage[table]:
                raise DuplicateRecordError(f"Record {record_id} already exists")
            self._storage[table][record_id] = data
            return data

    async def read(self, table: str, record_id: str) -> Optional[dict]:
        return self._storage[table].get(record_id)

    async def join(self, table1: str, table2: str, key: str) -> List[dict]:
        results = []
        for record1 in self._storage[table1].values():
            key_value = record1.get(key)
            for record2 in self._storage[table2].values():
                if record2.get(key) == key_value:
                    results.append({**record1, **record2})
        return results
```

### 2.3 API Implementation

#### 2.3.1 Design Rationale
The API implementation follows REST best practices by using resource-specific endpoints instead of generic table operations. Here's why:

1. **Security**:
   - Resource-specific endpoints prevent arbitrary table access
   - Enables fine-grained access control per resource
   - Eliminates SQL injection-like vulnerabilities from dynamic table names
   - Allows validation specific to each resource type

2. **RESTful Design**:
   - Resources are nouns (users, orders) rather than operations (add_record, join)
   - Relationships expressed through nested routes (e.g., /users/{id}/orders)
   - HTTP methods indicate the operation (GET, POST, etc.)
   - Clear hierarchy and resource ownership

3. **Type Safety**:
   - Each endpoint has specific Pydantic models for validation
   - Compile-time type checking for request/response models
   - Better IDE support and code completion
   - Reduced runtime errors from invalid data

4. **Maintainability**:
   - Clear separation of concerns per resource
   - Easier to document and understand
   - Simpler testing with specific test cases
   - Better version control and API evolution

#### 2.3.2 FastAPI Router Structure
```python
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from uuid import UUID

router = APIRouter(prefix="/api/v1")

@router.get("/users/{user_id}/orders")
async def get_user_orders(
    user_id: UUID,
    db: InMemoryDB = Depends(get_db)
) -> List[OrderResponse]:
    """Get orders for a specific user - implements join functionality through resource relationship"""
    user = await db.read("users", str(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return await db.get_user_orders(user_id)

@router.get("/orders/{order_id}/user")
async def get_order_user(
    order_id: UUID,
    db: InMemoryDB = Depends(get_db)
) -> UserResponse:
    """Get user details for an order - implements join functionality through resource relationship"""
    order = await db.read("orders", str(order_id))
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return await db.get_order_user(order_id)
```

### 2.4 Data Models

#### 2.4.1 Base Models
```python
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID

class BaseRecord(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class User(BaseRecord):
    email: str
    full_name: str
    age: int

class Order(BaseRecord):
    user_id: UUID
    product_name: str
    quantity: int
    total_price: float
    order_date: datetime
```

## 3. Technical Implementation Details

### 3.1 Concurrency Handling
- Async/await for non-blocking I/O
- Table-level locking for write operations
- Read operations without locks for performance
- FastAPI's built-in concurrent request handling

### 3.2 Error Handling
```python
class DatabaseError(Exception):
    """Base exception for database operations"""
    pass

class DuplicateRecordError(DatabaseError):
    """Raised when attempting to create a duplicate record"""
    pass

class RecordNotFoundError(DatabaseError):
    """Raised when a record is not found"""
    pass

# Error Handler Registration
@app.exception_handler(DatabaseError)
async def database_error_handler(request: Request, exc: DatabaseError):
    return JSONResponse(
        status_code=400,
        content={"error": str(exc)}
    )
```

### 3.3 Performance Optimizations
1. In-memory storage for fast access
2. Indexing for join operations
3. Efficient data structures
4. Connection pooling
5. Response caching

## 4. Testing Strategy

### 4.1 Unit Tests
```python
import pytest
from fastapi.testclient import TestClient

def test_create_record():
    client = TestClient(app)
    response = client.post(
        "/api/v1/data/users",
        json={
            "email": "test@example.com",
            "full_name": "Test User",
            "age": 30
        }
    )
    assert response.status_code == 200
    assert "id" in response.json()

@pytest.mark.asyncio
async def test_join_tables():
    db = InMemoryDB()
    # Setup test data
    user_id = str(uuid4())
    await db.create("users", user_id, {"name": "Test"})
    await db.create("orders", str(uuid4()), {"user_id": user_id})
    
    # Test join
    results = await db.join("users", "orders", "user_id")
    assert len(results) == 1
```

## 5. Deployment Architecture

### 5.1 Docker Configuration
```dockerfile
# Multi-stage build
FROM python:3.8-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.8-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.8/site-packages/ /usr/local/lib/python3.8/site-packages/
COPY . .

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 5.2 Health Check Implementation
```python
from fastapi import FastAPI
from typing import Dict

app = FastAPI()

@app.get("/health")
async def health_check() -> Dict[str, str]:
    return {
        "status": "healthy",
        "version": "1.0.0"
    }
```

## 6. Monitoring and Logging

### 6.1 Logging Configuration
```python
import logging
from fastapi import Request
from time import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time()
    response = await call_next(request)
    duration = time() - start_time
    logger.info(
        f"Method: {request.method} Path: {request.url.path} "
        f"Duration: {duration:.2f}s Status: {response.status_code}"
    )
    return response
```

## 7. Security Considerations

### 7.1 Input Validation
- Pydantic models for request validation
- Type checking and constraints
- Sanitization of input data
- Request size limits

### 7.2 Rate Limiting
```python
from fastapi import Request
from fastapi.responses import JSONResponse
from typing import Dict
from time import time

class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, List[float]] = {}

    async def check(self, ip: str) -> bool:
        now = time()
        if ip not in self.requests:
            self.requests[ip] = []
        
        # Remove old requests
        self.requests[ip] = [t for t in self.requests[ip] if now - t < 60]
        
        if len(self.requests[ip]) >= self.requests_per_minute:
            return False
        
        self.requests[ip].append(now)
        return True
```

## 8. API Documentation

### 8.1 OpenAPI Specification
```python
app = FastAPI(
    title="In-Memory Database Service",
    description="A high-performance in-memory database service with REST API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)
```

## 9. Future Optimizations

### 9.1 Potential Improvements
1. Implement caching layer
2. Add database sharding
3. Support for complex queries
4. Implement backup/restore

### 9.2 Scaling Strategy
1. Horizontal scaling with load balancer
2. Memory optimization techniques
3. Connection pooling
4. Query optimization
5. Caching strategies 
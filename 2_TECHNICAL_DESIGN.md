# Technical Design Document: In-Memory Database Service

## Table of Contents
- [1. System Architecture](#1-system-architecture)
  - [1.1 High-Level Architecture](#11-high-level-architecture)
  - [1.2 Component Overview](#12-component-overview)
- [2. Detailed Design](#2-detailed-design)
  - [2.1 Project Structure](#21-project-structure)
    - [2.1.1 Application Directory](#211-application-directory-app)
    - [2.1.2 Test Directory](#212-test-directory-tests)
  - [2.2 Model Hierarchy and Layer Analysis](#22-model-hierarchy-and-layer-analysis)
    - [2.2.1 Layer Dependencies and Project Structure](#221-layer-dependencies-and-project-structure)
    - [2.2.2 Layer-by-Layer Analysis](#222-layer-by-layer-analysis)
    - [2.2.3 Design Principles](#223-design-principles)
    - [2.2.4 Interaction Flow Examples](#224-interaction-flow-examples)
  - [2.3 Data Storage Implementation](#23-data-storage-implementation)
    - [2.3.1 In-Memory Database Class](#231-in-memory-database-class)
    - [2.3.2 Singleton Pattern Implementation](#232-singleton-pattern-implementation)
- [3. Technical Implementation Details](#3-technical-implementation-details)
  - [3.1 Concurrency Handling](#31-concurrency-handling)
  - [3.2 Performance Optimizations](#32-performance-optimizations)
- [4. Testing Strategy](#4-testing-strategy)
  - [4.1 Test Organization](#41-test-organization)
  - [4.2 Test Implementation Details](#42-test-implementation-details)
    - [4.2.1 Normal Path Testing](#421-normal-path-testing)
- [5. Deployment](#5-deployment)
- [6. Security Considerations](#6-security-considerations)
- [7. Future Optimizations](#7-future-optimizations)

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

#### 2.1.1 Application Directory (@app)
The application follows a clean architecture pattern with clear separation of concerns:

```
@app
├── __init__.py      # Package initialization
├── main.py          # Application entry point (FastAPI app configuration)
├── utils.py         # Utility functions and helpers
├── api/             # API routes/endpoints
│   ├── v1/          # API version 1
│   └── deps.py      # Dependency injections
├── core/            # Core application configuration
├── db/              # Database related code
├── models/          # Database models
├── schemas/         # Pydantic models
└── services/        # Business logic layer
```

#### 2.1.2 Test Directory (@tests)
The test suite is organized to cover different testing scenarios:

```
@tests
├── __init__.py                  # Test package initialization
├── test_api_normal.py           # Normal path test cases
├── test_api_edge_cases.py       # Edge case test scenarios
├── test_api_performance.py      # Performance test suite
├── generate_test_report.py      # Test report generation utility
├── sample_data.json             # Test data fixtures
└── test_reports/               # Generated test reports
```

### 2.2 Model Hierarchy and Layer Analysis

#### 2.2.1 Layer Dependencies and Project Structure
```
@app
├── db/      (lowest)  → Pure data storage, no app dependencies
├── models/           → Core data structures
├── schemas/         → API data validation
├── services/        → Business logic
└── api/    (highest) → API endpoints and routing
```

#### 2.2.2 Layer-by-Layer Analysis

##### @db (Lowest Level)
- **Description**: Core database operations with table-level locking and concurrency support
- **Key Characteristics**:
  - Implements Singleton pattern for single database instance
  - Table-level locking using asyncio.Lock
  - Thread-safe concurrent operations
  - Clear error hierarchy with custom exceptions
  - Async/await support for all operations
- **Key Files**:
  - `base.py`: Core InMemoryDB implementation with:
    - CRUD operations with table-level locking
    - Singleton pattern implementation
    - Custom error types (DatabaseError, DuplicateRecordError, etc.)
  - `initial_data.py`: Seed data and initialization
  - `sample_data.json`: Sample data for development/testing
- **Dependencies**: Standard library only (collections, typing, asyncio)
- **Evaluation**: Strong implementation of concurrent data access patterns and error handling

##### @models
- **Description**: Core data structures and domain models
- **Key Characteristics**:
  - Defines domain entities and relationships
  - Implements business rules and constraints
  - Used by services layer for data manipulation
- **Key Files**:
  - Domain model definitions
  - Data validation rules
  - Entity relationships
- **Dependencies**: Minimal external dependencies
- **Evaluation**: Clear separation of domain logic from other concerns

##### @schemas
- **Description**: API-specific data validation and serialization
- **Key Characteristics**:
  - Pydantic models for request/response validation
  - Clear separation between input and output schemas
  - Detailed field validation and documentation
  - Example data for API documentation
- **Key Files**:
  - `user.py`: User-related schemas with:
    - Input validation (UserCreate, UserUpdate)
    - Response formatting (UserResponse)
    - Field documentation and examples
- **Dependencies**: Pydantic, domain models
- **Evaluation**: Well-structured data validation with good API documentation support

##### @services (High Level)
- **Description**: Business logic and transaction management
- **Key Characteristics**:
  - Implements use cases and business rules
  - Handles data transformation and validation
  - Manages transactions and error handling
  - Provides clean interface for API layer
- **Key Files**:
  - `user_service.py`: User operations with:
    - CRUD operations with proper error handling
    - Data transformation between schemas and storage
    - Business logic implementation
    - Async operation support
- **Dependencies**: @db, @models, @schemas
- **Evaluation**: Clean separation of business logic with proper error handling

##### @api (Highest Level)
- **Description**: HTTP interface and request handling
- **Key Characteristics**:
  - Versioned API endpoints (v1)
  - Dependency injection setup
  - Request/response handling
  - Error translation to HTTP responses
- **Key Files**:
  - `v1/`: API version 1 endpoints
  - `deps.py`: Dependency injection configuration
  - `main.py`: API route registration
- **Dependencies**: @services, @schemas
- **Evaluation**: Well-organized API structure with proper versioning

##### @core
- **Description**: Application configuration and shared utilities
- **Key Characteristics**:
  - Environment configuration
  - Application settings
  - Shared constants and utilities
- **Key Files**:
  - `config.py`: Application configuration
- **Dependencies**: Minimal external dependencies
- **Evaluation**: Centralized configuration management

##### @utils
- **Description**: Shared utility functions and helpers
- **Key Characteristics**:
  - Common utility functions
  - Shared helper methods
  - Reusable components
- **Key Files**:
  - `utils.py`: Utility functions and helpers
- **Dependencies**: Standard library
- **Evaluation**: Good separation of reusable functionality

#### 2.2.3 Design Principles

1. **Separation of Concerns**:
   - Each directory has a specific responsibility
   - Clear boundaries between components
   - Minimal coupling between modules
   - Maximum cohesion within modules

2. **Dependency Management**:
   - Centralized dependency injection
   - Clear dependency flow
   - Easy to test and mock
   - Configurable dependencies

3. **Scalability**:
   - Easy to add new features
   - Simple to maintain
   - Clear upgrade paths
   - Version control friendly

#### 2.2.4 Interaction Flow Examples

1. **Creating a User**:
```
API Route → UserService.create_user(user_data: User) →
    → user_data.model_dump() [from @models] →
        → InMemoryDB.create("users", user_id, user_dict) [from @db]
```

2. **Getting User Orders**:
```
API Route → OrderService.get_user_orders(user_id: UUID) →
    → InMemoryDB.list("orders") [from @db] →
        → Filter orders by user_id [in service layer]
```

### 2.3 Data Storage Implementation

#### 2.3.1 In-Memory Database Class
The core database functionality is implemented in [db/base.py](./db/base.py) which provides:
- Singleton pattern implementation
- Table-level locking for concurrent operations
- Async/await support
- Generic CRUD operations
- Custom error handling

#### 2.3.2 Singleton Pattern Implementation
The in-memory database uses the Singleton pattern to ensure only one database instance exists throughout the application lifecycle. This is crucial for maintaining consistent state across all API endpoints.

1. **Core Implementation in `InMemoryDB`**:
See implementation in [db/base.py](./db/base.py)

2. **Usage in FastAPI Application**:
See implementation in [main.py](./main.py)

3. **Dependency Injection**:
See implementation in [api/deps.py](./api/deps.py)

The Singleton pattern ensures:
- Only one database instance exists application-wide
- All API endpoints work with the same data store
- Consistent state management across requests
- Thread-safe initialization and access
- Efficient memory usage by preventing multiple instances
- Simplified dependency injection in FastAPI

## 3. Technical Implementation Details

### 3.1 Concurrency Handling
- Async/await for non-blocking I/O
- Table-level locking for write operations
- Read operations without locks for performance
- FastAPI's built-in concurrent request handling

### 3.2 Performance Optimizations
1. In-memory storage for fast access
2. Efficient data structures
3. Connection pooling
4. Response caching

## 4. Testing Strategy

### 4.1 Test Organization

The test suite is organized into three distinct categories:

1. **Normal Path Tests** (`test_api_normal.py`)
   - Basic CRUD operations
   - List operations
   - Resource relationships
   - Data validation

2. **Edge Case Tests** (`test_api_edge_cases.py`)
   - Error handling
   - Invalid input data
   - Resource state transitions
   - Concurrent modifications

3. **Performance Tests** (`test_api_performance.py`)
   - Single operation timing (< 50ms)
   - Bulk operations (< 500ms)
   - Concurrent operations (50 requests < 5s)
   - Resource usage monitoring

### 4.2 Test Implementation Details

#### 4.2.1 Normal Path Testing
- **Purpose**: Verify correct behavior under expected conditions
- **Coverage**: All API endpoints and data operations
- **Validation**: Data consistency and response formats
- **Tools**: pytest, FastAPI TestClient

#### 4.2.2 Edge Case Testing
- **Purpose**: Verify system behavior under unexpected conditions
- **Coverage**: Error handling and boundary conditions
- **Validation**: Error responses and system stability
- **Focus Areas**:
  - Invalid input handling
  - Resource state transitions
  - Concurrent access patterns
  - Error message accuracy

#### 4.2.3 Performance Testing
- **Purpose**: Verify system performance under various conditions
- **Tools**: pytest-benchmark, ThreadPoolExecutor
- **Metrics**:
  - Response times
  - Concurrent operation handling
  - Resource utilization
  - Operation throughput

### 4.3 Test Execution Strategy

#### 4.3.1 Local Development
Available in Makefile:
```bash
# Normal path tests
make test-normal

# Edge case tests
make test-edge

# Performance tests
make test-performance
```

## 5. Deployment

For detailed deployment information, including Docker configuration, deployment scenarios, resource management, and maintenance procedures, please refer to the [Deployment Guide](./deploy/DEPLOYMENT.md).

The deployment documentation covers:
- Multi-stage Docker build architecture
- Container orchestration with Docker Compose
- Development and production deployment scenarios
- Resource management and monitoring
- Health checks and logging
- Maintenance procedures

## 6. Security Considerations

### 6.1 Input Validation
- Pydantic models for request validation
- Type checking and constraints
- Sanitization of input data

## 7. Future Optimizations

### 7.1 Potential Improvements
1. Advanced Monitoring Features:
   - OpenTelemetry integration
   - Distributed tracing
   - Metrics collection
   - Custom dashboards
   - Advanced health checks

2. Security Enhancements:
   - Rate limiting middleware
   - API key management
   - Request signing
   - Security audit logging
   - Advanced threat detection

3. Performance Optimizations:
   - Caching layer
   - Database sharding
   - Complex query support
   - Connection pooling optimization
   - Query optimization

4. Reliability Features:
   - Data persistence
   - Backup/restore system
   - Circuit breaker pattern
   - Failover mechanisms
   - Data consistency checks

5. Authentication & Authorization:
   - JWT authentication
   - Role-based access control
   - Session management
   - Password hashing
   - Token management

### 7.2 Scaling Strategy
1. Horizontal scaling
2. Memory optimization
3. Load balancer integration
4. Auto-scaling configuration
5. Resource usage optimization


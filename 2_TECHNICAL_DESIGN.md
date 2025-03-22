# Technical Design Document: In-Memory Database Service

## Table of Contents
- [System Architecture](#1-system-architecture)
- [Detailed Design](#2-detailed-design)
- [Technical Implementation Details](#3-technical-implementation-details)
- [Testing Strategy](#4-testing-strategy)
- [Deployment Architecture](#5-deployment-architecture)
- [Security Considerations](#6-security-considerations)
- [Future Optimizations](#7-future-optimizations)

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

#### 2.1.3 Component Responsibilities

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

6. **tests/**
   - `test_api_normal.py`: Basic functionality and happy path scenarios
   - `test_api_edge_cases.py`: Error handling and boundary conditions
   - `test_api_performance.py`: Load testing and performance benchmarks
   - `generate_test_report.py`: Automated test report generation
   - `test_reports/`: Storage for test execution results
   - `sample_data.json`: Test data for consistent test execution

#### 2.1.4 Design Principles

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
See implementation in [db/base.py](./db/base.py)

#### 2.2.2 Singleton Pattern Implementation
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

## 5. Deployment Architecture

### 5.1 Docker Configuration
The service uses a multi-stage Docker build process optimized for both development and production environments.

#### 5.1.1 Multi-Stage Build Architecture
1. **Builder Stage**
   - Python 3.11-slim base image
   - UV package manager (v0.5.11)
   - Build dependencies installation
   - Dependency management with UV sync
   - Bytecode compilation enabled

2. **Development Stage**
   - Inherits from builder
   - Development environment settings
   - Hot-reload with Uvicorn
   - Debug mode enabled
   - Source code mounting

3. **Production Stage**
   - Minimal Python 3.11-slim image
   - Non-root user execution
   - Resource limits:
     - Memory: 512MB
     - CPU: 1.0 cores
   - 4 Gunicorn workers
   - Health check implementation

#### 5.1.2 Container Orchestration
Docker Compose configuration includes:
1. Build configuration with target selection
2. Resource management (CPU/memory limits)
3. Environment variable configuration
4. Health monitoring
5. Log rotation
6. Network isolation

### 5.2 Health Check Implementation
- Basic health check endpoint at `/api/v1/utils/health-check`
- Docker health check configuration:
  - 30-second interval
  - 5-second timeout
  - 3 retries
  - 5-second start period

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


# Technical Design Document: In-Memory Database Service

## Table of Contents
- [1. System Architecture](#1-system-architecture)
  - [1.1 High-Level Architecture](#11-high-level-architecture)
  - [1.2 Component Overview](#12-component-overview)
  - [1.3 Project Structure](#13-project-structure)
  - [1.4 Model Hierarchy and Layer Analysis](#14-model-hierarchy-and-layer-analysis)
    - [1.4.1 Layer Dependencies and Project Structure](#141-layer-dependencies-and-project-structure)
    - [1.4.2 Layer-by-Layer Analysis](#142-layer-by-layer-analysis)
    - [1.4.3 Design Principles](#143-design-principles)
    - [1.4.4 Interaction Flow Examples](#144-interaction-flow-examples)
- [2. Design and Implementation Details](#2-design-and-implementation-details)
  - [2.1 Data Storage Implementation](#21-data-storage-implementation)
    - [2.1.1 In-Memory Database Class](#211-in-memory-database-class)
    - [2.1.2 Singleton Pattern Implementation](#212-singleton-pattern-implementation)
  - [2.2 Concurrency Handling](#22-concurrency-handling)
    - [2.2.1 Table-Level Locking](#221-table-level-locking)
    - [2.2.2 Async Operations](#222-async-operations)
- [3. Performance Optimizations](#3-performance-optimizations)
  - [3.1 Index Optimization](#31-index-optimization)
  - [3.2 Test Results of Index Optimization](#32-test-results-of-index-optimization)
    - [3.2.1 Summary of Performance Improvements](#321-summary-of-performance-improvements)
    - [3.2.2 Key Performance Improvements](#322-key-performance-improvements)
    - [3.2.3 Theoretical Explanation](#323-theoretical-explanation)
  - [3.3 Future Optimizations](#33-future-optimizations)
- [4. Testing Strategy](#4-testing-strategy)
- [5. Deployment](#5-deployment)
- [6. Security Considerations](#6-security-considerations)
  - [6.1 Input Validation](#61-input-validation)
  - [6.2 Rate Limiting](#62-rate-limiting)
  - [6.3 Error Handling](#63-error-handling)
- [7. Future Optimizations](#7-future-optimizations)
  - [7.1 Planned Improvements](#71-planned-improvements)
  - [7.2 Scaling Strategy](#72-scaling-strategy)
  - [7.3 Known Limitations](#73-known-limitations)

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

### 1.3 Project Structure
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

### 1.4 Model Hierarchy and Layer Analysis

The application follows a layered architecture that promotes separation of concerns, maintainability, and testability. Each layer has a specific responsibility and communicates with other layers through well-defined interfaces. The architecture is built on three core design principles:

1. **Separation of Concerns**
   - Each layer has a specific responsibility and clear boundaries
   - Components are modular with minimal coupling between them
   - Maximum cohesion within modules ensures focused functionality
   - Clear interfaces between layers maintain clean architecture

2. **Dependency Management**
   - Centralized dependency injection for flexible component wiring
   - Clear dependency flow from high-level to low-level modules
   - Easy to test and mock components in isolation
   - Configurable dependencies for different environments

3. **Scalability and Maintainability**
   - Easy to add new features without modifying existing code
   - Simple to maintain with clear upgrade paths
   - Version control friendly architecture
   - Flexible implementation details within each layer

The architecture is designed to be:
- **Maintainable**: Clear separation between layers makes it easy to modify or replace components
- **Testable**: Each layer can be tested in isolation with mock dependencies
- **Scalable**: New features can be added without modifying existing code
- **Flexible**: Implementation details can be changed without affecting other layers
- **Secure**: Business logic and data access are properly encapsulated

The layers are organized in a hierarchical structure, with each layer depending only on the layers below it. This ensures a clean and maintainable codebase with minimal coupling between components.

#### 1.4.1 Layer Dependencies and Project Structure
```
@app
├── db/      (lowest)  → Pure data storage, no app dependencies
├── models/           → Core data structures
├── schemas/         → API data validation
├── services/        → Business logic
└── api/    (highest) → API endpoints and routing
```

#### 1.4.2 Layer-by-Layer Analysis

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

#### 1.4.3 Design Principles

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

#### 1.4.4 Interaction Flow Examples

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

## 2. Design and Implementation Details

### 2.1 Data Storage Implementation

#### 2.1.1 In-Memory Database Class
The core database functionality is implemented in [db/base.py](./db/base.py) which provides:
- Singleton pattern implementation
- Table-level locking for concurrent operations
- Async/await support
- Generic CRUD operations
- Custom error handling

#### 2.1.2 Singleton Pattern Implementation
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

### 2.2 Concurrency Handling

#### 2.2.1 Table-Level Locking
- Implemented using `asyncio.Lock` for each table
- Write operations (create, update, delete) protected by table-specific locks
- Read operations don't acquire locks for better performance
- Operations on different tables can proceed concurrently
- Deadlock prevention through consistent lock acquisition order

#### 2.2.2 Async Operations
- Async/await for non-blocking I/O operations
- FastAPI's built-in concurrent request handling
- Asynchronous database operations
- Efficient resource utilization during I/O-bound operations
- Non-blocking request processing

## 3. Performance Optimizations

For comprehensive details about performance optimizations, including implementation details, test results, and future plans, please refer to our [Performance Optimization Guide](./3_PERFORMANCE_OPTIMIZATION.md).

Key highlights of our performance improvements:

1. **Hash-Based Indexing**
   - Implemented efficient hash indexing for exact-match queries
   - Achieved significant performance gains:
     - 59.9% faster worst-case user retrieval operations
     - 43.3% improvement in table dump maximum latency 
     - 16.3% better worst-case relationship query performance
     - 7.8% improvement in mean latency for table dumps
     - 10.9% increase in operations per second for relationship endpoints
   - O(1) lookup time for indexed fields with minimal memory overhead

2. **Current Focus Areas**
   - Relationship-based query optimization
   - Memory-efficient data structures
   - Table-level operation performance
   - Query response time improvements

3. **Upcoming Optimizations**
   - Advanced caching strategies
   - Query result pagination
   - Additional index features
   - Memory optimization techniques

For detailed implementation specifics, theoretical background, test results, and future optimization plans, see the [Performance Optimization Guide](./3_PERFORMANCE_OPTIMIZATION.md).

## 4. Testing Strategy

For detailed testing information, including test organization, implementation details, execution strategy, and reporting, please refer to the [Testing Strategy](./backend/tests/TESTING_STRATEGY.md) document.

## 5. Deployment

For detailed deployment information, including Docker configuration, deployment scenarios, resource management, monitoring, health checks, logging, and maintenance procedures, please refer to the [Deployment Guide](./deploy/DEPLOYMENT.md) document.

## 6. Security Considerations

### 6.1 Input Validation
- Pydantic models for request validation
- Type checking and constraints
- Sanitization of input data

### 6.2 Rate Limiting
- Implement rate limiting middleware
- Use Redis for distributed rate limiting

### 6.3 Error Handling
- Implement circuit breaker pattern
- Use retry logic with exponential backoff

## 7. Future Optimizations

### 7.1 Planned Improvements
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

### 7.3 Known Limitations
1. Single-node deployment
2. Limited scalability
3. No distributed transactions
4. No ACID compliance


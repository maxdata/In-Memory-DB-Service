# In-Memory Database Service

## Table of Contents
- [1. Overview](#1-overview)
- [2. Project Document Structure](#2-project-document-structure)
  - [2.1 README.md](#21-readmemd)
  - [2.2 Product Requirements](#22-product-requirements)
  - [2.3 Technical Design](#23-technical-design)
  - [2.4 Performance Optimization](#24-performance-optimization)
  - [2.5 Contributing Guide](#25-contributing-guide)
  - [2.6 Test Strategy](#26-test-strategy)
  - [2.7 Deployment Guide](#27-deployment-guide)
- [3. Quick Start](#3-quick-start)
  - [3.1 Installation & Usage](#31-installation--usage)
  - [3.2 Common Make Commands](#32-common-make-commands)
  - [3.3 Code Quality](#33-code-quality)
- [4. Technical Design](#4-technical-design)
- [5. Performance Optimization](#5-performance-optimization)
- [6. Testing](#6-testing)
- [7. Deployment](#7-deployment)
- [8. API Documentation](#8-api-documentation)
  - [8.1 API Reference](#81-api-reference)
  - [8.2 User Operations](#82-user-operations)
  - [8.3 Order Operations](#83-order-operations)
  - [8.4 Relationship Operations](#84-relationship-operations)
  - [8.5 Table Operations](#85-table-operations)

## 1. Overview

This service provides a production-ready foundation for building RESTful APIs with FastAPI, featuring in-memory data storage and comprehensive testing capabilities. The service supports basic database operations (CRUD) and allows for simple join operations between datasets.

## 2. Project Document Structure

### 2.1 README.md
[`./README.md`](./README.md)  
Primary entry point for the project, containing quick start guide, installation instructions, and overview of all features and components.

### 2.2 Product Requirements
[`./1_PRODUCT_REQUIREMENTS.md`](./1_PRODUCT_REQUIREMENTS.md)  
Comprehensive documentation of product features, user stories, acceptance criteria, and business requirements.

### 2.3 Technical Design
[`./2_TECHNICAL_DESIGN.md`](./2_TECHNICAL_DESIGN.md)  
Detailed technical architecture, system design, implementation specifications, and architectural decisions.

### 2.4 Performance Optimization
[`./3_PERFORMANCE_OPTIMIZATION.md`](./3_PERFORMANCE_OPTIMIZATION.md)  
Comprehensive performance optimization strategies, test results, and future optimization plans.

### 2.5 Contributing Guide
[`./4_CONTRIBUTING.md`](./4_CONTRIBUTING.md)  
Development standards, workflow guidelines, and contribution procedures for developers.

### 2.6 Test Strategy
[`./backend/tests/TESTING_STRATEGY.md`](./backend/tests/TESTING_STRATEGY.md)  
Testing methodology, test organization, and execution guidelines.

### 2.7 Deployment Guide
[`./deploy/DEPLOYMENT.md`](./deploy/DEPLOYMENT.md)  
Complete deployment procedures, environment setup, and operational instructions.

## 3. Quick Start

### 3.1 Installation & Usage

1. Clone the repository:
```bash
git clone https://github.com/yourusername/in-memory-db-service.git
cd in-memory-db-service
```

2. View available commands:
```bash
make help
```

3. Quick development setup:
```bash
make dev  # Installs dependencies, formats code, runs linter and tests, starts the server
```

### 3.2 Common Make Commands

| Command | Description |
|---------|-------------|
| `make install` | Install dependencies |
| `make run` | Run the application locally |
| `make test` | Run all tests |
| `make test-report` | Generate comprehensive test report |
| `make clean` | Clean up temporary files |

### 3.3 Code Quality

| Command | Tool | Description |
|---------|------|-------------|
| `make format` | Black | Automatically format Python code to match PEP 8 style |
| `make lint` | Flake8 | Check code style and quality for potential errors |

## 4. Technical Design

For detailed technical specifications and architecture details, please refer to our comprehensive [Technical Design Document](./2_TECHNICAL_DESIGN.md). The document covers:

- [System Architecture](./2_TECHNICAL_DESIGN.md#1-system-architecture)
  - High-Level Architecture
  - Component Overview
  - Project Structure
  - Model Hierarchy and Layer Analysis
    - Layer Dependencies and Project Structure
    - Layer-by-Layer Analysis
    - Design Principles
    - Interaction Flow Examples
- [Design and Implementation Details](./2_TECHNICAL_DESIGN.md#2-design-and-implementation-details)
  - Data Storage Implementation
    - In-Memory Database Class
    - Singleton Pattern Implementation
  - Concurrency Handling
    - Table-Level Locking
    - Async Operations
- [Performance Optimizations](./2_TECHNICAL_DESIGN.md#3-performance-optimizations)
  - Index Optimization
  - Test Results of Index Optimization
  - Future Optimizations
- [Testing Strategy](./2_TECHNICAL_DESIGN.md#4-testing-strategy)
- [Deployment](./2_TECHNICAL_DESIGN.md#5-deployment)
- [Security Considerations](./2_TECHNICAL_DESIGN.md#6-security-considerations)
  - Input Validation
  - Rate Limiting
  - Error Handling
- [Future Optimizations](./2_TECHNICAL_DESIGN.md#7-future-optimizations)
  - Planned Improvements
  - Scaling Strategy
  - Known Limitations

Key technical features include:
- In-memory data storage with table-level locking
- Singleton pattern implementation for database consistency
- Hash-based indexing with proven performance improvements
- Async/await support for non-blocking operations
- RESTful API with FastAPI framework
- Comprehensive error handling and validation
- Efficient data relationship management

For implementation details and guidelines, see:
- [Data Storage Implementation](./2_TECHNICAL_DESIGN.md#21-data-storage-implementation)
- [Concurrency Handling](./2_TECHNICAL_DESIGN.md#22-concurrency-handling)
- [Index Optimization](./2_TECHNICAL_DESIGN.md#31-index-optimization)
- [Performance Test Results](./2_TECHNICAL_DESIGN.md#32-test-results-of-index-optimization)

## 5. Performance Optimization

For detailed performance optimization strategies and benchmarks, please refer to our [Performance Optimization Document](./3_PERFORMANCE_OPTIMIZATION.md). The document covers:

- [Index Optimization](./3_PERFORMANCE_OPTIMIZATION.md#2-index-optimization)
- [Performance Test Results](./3_PERFORMANCE_OPTIMIZATION.md#3-performance-test-results)

Key performance improvements include:
- Hash-based indexing implementation with proven improvements:
  - 59.9% faster worst-case user retrieval operations
  - 43.3% improvement in table dump maximum latency
  - 16.3% better worst-case relationship query performance
  - 7.8% improvement in mean latency for table dumps
  - 10.9% increase in operations per second for relationship endpoints
- O(1) lookup time for indexed fields with minimal memory overhead

Current focus areas include:
- Relationship-based query optimization
- Memory-efficient data structures
- Table-level operation performance
- Query response time improvements

Upcoming optimizations:
- Advanced caching strategies
- Query result pagination
- Additional index features
- Memory optimization techniques

For detailed metrics and implementation details, see:
- [Implementation Strategy](./3_PERFORMANCE_OPTIMIZATION.md#21-implementation-strategy)
- [Index Types and Considerations](./3_PERFORMANCE_OPTIMIZATION.md#22-index-types-and-considerations)
- [Performance Test Results](./3_PERFORMANCE_OPTIMIZATION.md#31-summary-of-improvements)
- [Theoretical Explanation](./3_PERFORMANCE_OPTIMIZATION.md#323-theoretical-explanation)

## 6. Testing

For comprehensive testing information, including test organization, implementation, execution, and reporting, please refer to our [Testing Strategy Document](./backend/tests/TESTING_STRATEGY.md).

The testing documentation covers:
- Test Directory Structure
- Test Categories and Organization
- Test Implementation Details
- Test Execution and Reporting
- Coverage Analysis
- Performance Testing

Quick reference for common test-related commands:
```bash
make test           # Run all tests
make test-report    # Generate comprehensive test report
```

## 7. Deployment

For detailed deployment instructions, configurations, and commands, please refer to our comprehensive [Deployment Guide](./deploy/DEPLOYMENT.md). The guide covers:

- [Quick Start and Installation](./deploy/DEPLOYMENT.md#1-quick-start)
- [Deployment Architecture](./deploy/DEPLOYMENT.md#2-deployment-architecture)
- [Deployment Scenarios](./deploy/DEPLOYMENT.md#3-deployment-scenarios)
- [Resource Management](./deploy/DEPLOYMENT.md#4-resource-management)
- [Health Checks](./deploy/DEPLOYMENT.md#5-health-checks)
- [Logging](./deploy/DEPLOYMENT.md#6-logging)
- [Maintenance](./deploy/DEPLOYMENT.md#8-maintenance)

For quick reference to deployment commands, see:
- [Common Make Commands](./deploy/DEPLOYMENT.md#12-common-make-commands)
- [Docker Commands](./deploy/DEPLOYMENT.md#34-docker-commands)

## 8. API Documentation

### 8.1 API Reference

| Documentation Type | URL | Description |
|-------------------|-----|-------------|
| Swagger UI | `http://localhost:8000/docs` | Interactive API documentation with testing capability |
| ReDoc | `http://localhost:8000/redoc` | Alternative API documentation with better readability |

Below are examples of how to interact with the API using cURL. All responses are in JSON format.

### 8.2 User Operations

1. Create a new user:
```bash
curl -X POST http://localhost:8000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "full_name": "John Doe",
    "password": "securepass123"
  }'
```

2. Get a user by ID:
```bash
curl -X GET http://localhost:8000/api/v1/users/550e8400-e29b-41d4-a716-446655440000
```

### 8.3 Order Operations

1. Create a new order:
```bash
curl -X POST http://localhost:8000/api/v1/orders \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "amount": 99.99,
    "description": "Premium Package",
    "status": "pending"
  }'
```

2. Get an order by ID:
```bash
curl -X GET http://localhost:8000/api/v1/orders/550e8400-e29b-41d4-a716-446655441111
```

### 8.4 Relationship Operations

1. Get all orders for a user:
```bash
curl -X GET http://localhost:8000/api/v1/users/550e8400-e29b-41d4-a716-446655440000/orders
```

2. Get user associated with an order:
```bash
curl -X GET http://localhost:8000/api/v1/orders/550e8400-e29b-41d4-a716-446655441111/user
```

### 8.5 Table Operations

1. Dump table contents:
```bash
curl -X GET http://localhost:8000/api/v1/tables/users/dump  # For users table
curl -X GET http://localhost:8000/api/v1/tables/orders/dump # For orders table
```

Note: Replace the UUIDs in the examples with actual UUIDs from your system. All endpoints return appropriate HTTP status codes:
- 200: Successful operation
- 201: Resource created
- 400: Bad request
- 404: Resource not found
- 422: Validation error
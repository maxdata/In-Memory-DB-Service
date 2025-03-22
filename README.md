# In-Memory Database Service

## Table of Contents
- [Overview](#overview)
- [List of Documents](#list-of-documents)
- [Features](#features)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
  - [Installation & Usage](#installation--usage)
  - [Common Make Commands](#common-make-commands)
- [Development](#development)
  - [Code Quality](#code-quality)
  - [Running Tests](#running-tests)
  - [Tests Implementation](#tests-implementation)
- [API Documentation](#api-documentation)

## Overview

This service provides a production-ready foundation for building RESTful APIs with FastAPI, featuring in-memory data storage and comprehensive testing capabilities. The service supports basic database operations (CRUD) and allows for simple join operations between datasets.

## List of Documents

| Document | Path | Description |
|----------|------|-------------|
| Project Overview | [README.md](./README.md) | Main project documentation and getting started guide |
| Product Requirements | [1_PRODUCT_REQUIREMENTS.md](./1_PRODUCT_REQUIREMENTS.md) | Detailed product specifications and requirements |
| Technical Design | [2_TECHNICAL_DESIGN.md](./2_TECHNICAL_DESIGN.md) | System architecture and technical specifications |
| Test Reports | [backend/tests/test_reports](./backend/tests/test_reports) | Generated test reports with performance metrics |
| Deployment Guide | [deploy/DEPLOYMENT.md](./deploy/DEPLOYMENT.md) | Instructions for deployment and operations |
| API Documentation | `/docs` (when service is running) | Interactive API reference |
| Contributing Guide | [3_CONTRIBUTING.md](./3_CONTRIBUTING.md) | Guidelines for contributing to the project |

## Features

| Feature | Description |
|---------|-------------|
| FastAPI-based RESTful API | Production-ready service with well-structured endpoints |
| In-Memory Data Storage | Utilizes Python dictionaries for efficient data storage and retrieval |
| Data Models | Implements Pydantic models for robust data validation |
| CRUD Operations | Complete support for Create, Read, Update, and Delete operations |
| Join Functionality | Supports joining two datasets based on common keys |
| Comprehensive Testing | Includes unit tests covering all endpoints and edge cases |
| Docker Support | Fully containerized application for easy deployment |
| Make Commands | Unified interface for all development operations |

## Project Structure

```
in-memory-db-service/
├── backend/                # Main service implementation
│   ├── app/               # FastAPI application code
│   ├── tests/             # Test suite
│   └── scripts/           # Utility scripts
├── deploy/                # Deployment and infrastructure
├── .github/               # CI/CD and GitHub configurations
├── Makefile              # Development and build commands
├── 1_PRODUCT_REQUIREMENTS.md    # Product specifications
├── 2_TECHNICAL_DESIGN.md        # System architecture
├── 3_EVALUATION.yaml            # Quality criteria
├── 4_CONTRIBUTING.md            # Contribution guidelines
└── README.md             # Project overview
```

## Quick Start

### Installation & Usage

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

### Common Make Commands

| Command | Description |
|---------|-------------|
| `make install` | Install dependencies |
| `make test` | Run all tests |
| `make lint` | Run linter |
| `make format` | Format code |
| `make clean` | Clean up temporary files |
| `make run` | Run the application locally |
| `make docker-build` | Build Docker image |
| `make docker-run` | Run Docker container |

## Development

### Code Quality

| Command | Tool | Description |
|---------|------|-------------|
| `make format` | Black | Automatically format Python code to match PEP 8 style |
| `make lint` | Flake8 | Check code style and quality for potential errors |

### Running Tests

| Test Type | Command | Description |
|-----------|---------|-------------|
| Normal Tests | `make test-normal` | Run normal/happy path tests |
| Edge Cases | `make test-edge` | Run edge cases and error scenarios |
| Performance - Basic | `make performance-test` | Basic performance validation |
| Performance - Detailed | `make performance-benchmark` | Detailed benchmarks with statistics |
| Performance - Compare | `make performance-compare` | Compare with previous benchmark results |

### Tests Implementation

1. **Normal Tests** (`test_api_normal.py`)
   - Basic CRUD operations
   - Resource retrieval
   - List operations
   - Data validation
   - Relationship queries
   - Test results available in [backend/tests/test_reports](./backend/tests/test_reports)

2. **Edge Case Tests** (`test_api_edge_cases.py`)
   - Error handling scenarios
   - Invalid input validation
   - Boundary conditions
   - Resource conflicts
   - Missing data scenarios
   - Test results available in [backend/tests/test_reports](./backend/tests/test_reports)

3. **Performance Tests** (`test_api_performance.py`)
   - Load testing under various data sizes
   - Response time measurements
   - Memory usage monitoring
   - Concurrent request handling
   - Data structure efficiency
   - Join operation performance
   - Test results available in [backend/tests/test_reports](./backend/tests/test_reports)

Test reports are generated using `generate_test_report.py` and stored in the test_reports directory.

## API Documentation

| Documentation Type | URL | Description |
|-------------------|-----|-------------|
| Swagger UI | `http://localhost:8000/docs` | Interactive API documentation with testing capability |
| ReDoc | `http://localhost:8000/redoc` | Alternative API documentation with better readability |
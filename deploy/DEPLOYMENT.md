# Deployment Guide

## Table of Contents
- [1. Quick Start](#1-quick-start)
  - [1.1. Installation](#11-installation)
  - [1.2. Common Make Commands](#12-common-make-commands)
  - [1.3. Quick Development Setup](#13-quick-development-setup)
  - [1.4. Deployment Options](#14-deployment-options)
- [2. Deployment Architecture](#2-deployment-architecture)
  - [2.1. Docker Configuration](#21-docker-configuration)
    - [2.1.1. Multi-Stage Build Architecture](#211-multi-stage-build-architecture)
    - [2.1.2. Container Orchestration](#212-container-orchestration)
    - [2.1.3. Deployment File Organization](#213-deployment-file-organization)
  - [2.2. Package Management with UV](#22-package-management-with-uv)
    - [2.2.1. UV Configuration](#221-uv-configuration)
    - [2.2.2. Key Features](#222-key-features)
    - [2.2.3. Environment Management](#223-environment-management)
- [3. Deployment Scenarios](#3-deployment-scenarios)
  - [3.1. Local Development](#31-local-development)
  - [3.2. Production Deployment](#32-production-deployment)
  - [3.3. Environment Variables](#33-environment-variables)
  - [3.4. Docker Commands](#34-docker-commands)
    - [3.4.1. Development Environment](#341-development-environment)
    - [3.4.2. Production Environment](#342-production-environment)
    - [3.4.3. Docker Compose Commands](#343-docker-compose-commands)
    - [3.4.4. Environment Differences](#344-environment-differences)
- [4. Resource Management](#4-resource-management)
  - [4.1. Memory and CPU Limits](#41-memory-and-cpu-limits)
  - [4.2. Monitoring](#42-monitoring)
- [5. Health Checks](#5-health-checks)
- [6. Logging](#6-logging)
- [7. Documentation](#7-documentation)
  - [7.1. API Documentation](#71-api-documentation)
  - [7.2. Setup Instructions](#72-setup-instructions)
  - [7.3. Sample API Calls](#73-sample-api-calls)
  - [7.4. Troubleshooting Guide](#74-troubleshooting-guide)
- [8. Maintenance](#8-maintenance)
  - [8.1. Regular Tasks](#81-regular-tasks)
  - [8.2. Updates and Upgrades](#82-updates-and-upgrades)
- [9. Support](#9-support)

This guide covers various deployment scenarios and configurations for the In-Memory Database Service.

## 1. Quick Start

### 1.1. Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/in-memory-db-service.git
cd in-memory-db-service

# Install dependencies using UV package manager
uv sync
```

### 1.2. Common Make Commands

| Command | Description |
|---------|-------------|
| Development Commands |
| `make dev` | Quick start: Build and run development environment |
| `make docker-build-dev` | Build development Docker image |
| `make docker-run-dev` | Run development container with hot reload |
| `make docker-logs-dev` | Show development container logs |
| `make docker-shell-dev` | Open shell in development container |
| `make docker-test-dev` | Run tests in development container |
| `make docker-stop-dev` | Stop development container |
| `make docker-clean-dev` | Clean development Docker resources |
| Production Commands |
| `make prod` | Quick start: Build and run production environment |
| `make docker-build-prod` | Build production Docker image |
| `make docker-run-prod` | Run production container with resource limits |
| `make docker-logs-prod` | Show production container logs |
| `make docker-shell-prod` | Open shell in production container |
| `make docker-stop-prod` | Stop production container |
| `make docker-clean-prod` | Clean production Docker resources |
| Docker Compose Commands |
| `make compose-up-dev` | Start development environment with Docker Compose |
| `make compose-up-prod` | Start production environment with Docker Compose |
| `make compose-down` | Stop Docker Compose environment |

### 1.3. Quick Development Setup

```bash
# Start development environment
make dev

# Or using Docker Compose
make compose-up-dev
```

### 1.4. Deployment Options

1. **Local Development**
```bash
# Using Make command
make dev

# Or using Docker Compose
make compose-up-dev
```

2. **Production Deployment**
```bash
# Using Make command
make prod

# Or using Docker Compose
make compose-up-prod
```

## 2. Deployment Architecture

### 2.1. Docker Configuration
The service uses a multi-stage Docker build process optimized for both development and production environments.

#### 2.1.1. Multi-Stage Build Architecture

1. **Production Stage** (`Dockerfile`)
   - Python 3.11-slim base image
   - UV package manager (v0.5.11)
   - Non-root user execution (appuser)
   - Resource limits:
     - Memory: 512MB
     - CPU: 1.0 cores
   - 4 Gunicorn workers with Uvicorn worker class
   - Health check implementation
   - Environment variables:
     - `PYTHONUNBUFFERED=1`
     - `PYTHONDONTWRITEBYTECODE=1`
     - `ENVIRONMENT=production`
     - `DEBUG=false`
     - `WORKERS=4`
     - `PYTHONPATH=/app`

2. **Development Stage** (`Dockerfile.dev`)
   - Python 3.11-slim base image
   - Additional development tools:
     - build-essential
     - curl
     - git
   - Hot-reload with Uvicorn
   - Debug mode enabled
   - Environment variables:
     - `PYTHONUNBUFFERED=1`
     - `PYTHONDONTWRITEBYTECODE=1`
     - `ENVIRONMENT=development`
     - `DEBUG=true`
     - `PYTHONPATH=/app`

#### 2.1.2. Container Orchestration
Docker Compose configuration (`docker-compose.yml`) includes:
1. Build configuration with dynamic Dockerfile selection
   ```yaml
   dockerfile: ${DOCKERFILE:-Dockerfile}  # Use Dockerfile.dev for development
   ```
2. Resource management:
   ```yaml
   limits:
     cpus: '1.0'
     memory: 512M
   reservations:
     cpus: '0.25'
     memory: 256M
   ```
3. Environment variable configuration:
   ```yaml
   environment:
     - ENVIRONMENT=${ENVIRONMENT:-production}
     - DEBUG=${DEBUG:-false}
     - WORKERS=${WORKERS:-4}
     - CORS_ORIGINS=${CORS_ORIGINS:-http://localhost:8000}
   ```
4. Health monitoring:
   ```yaml
   healthcheck:
     test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/health"]
     interval: 30s
     timeout: 5s
     retries: 3
     start_period: 5s
   ```
5. Log rotation:
   ```yaml
   logging:
     driver: "json-file"
     options:
       max-size: "10m"
       max-file: "3"
   ```
6. Network isolation:
   ```yaml
   networks:
     default:
       driver: bridge
   ```

#### 2.1.3. Deployment File Organization
The deployment configuration follows a structured organization pattern:

```
project_root/
├── backend/
│   ├── Dockerfile        # Production configuration
│   └── Dockerfile.dev    # Development configuration
└── deploy/
    ├── docker-compose.yml    # Orchestration configuration
    └── DEPLOYMENT.md         # Deployment documentation
```

### 2.2. Package Management with UV

UV is the high-performance Python package installer and resolver used in this project. It provides several advantages:

#### 2.2.1. UV Configuration
- Version: 0.5.11 (in Docker build)
- Installation from GitHub Container Registry:
  ```dockerfile
  COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/
  ```
- Dependency installation with frozen resolution:
  ```dockerfile
  RUN --mount=type=cache,target=/root/.cache/uv \
      uv sync --frozen --no-install-project
  ```

#### 2.2.2. Key Features
1. **Dependency Resolution**
   - Fast, reliable dependency resolution
   - Uses `pyproject.toml` and `uv.lock` for dependency management
   - Frozen dependencies with `--frozen` flag for reproducible builds

2. **Development Setup**
   ```bash
   # Install dependencies
   uv sync
   
   # Install in editable mode
   uv install --editable .
   ```

3. **CI/CD Integration**
   - Integrated with GitHub Actions workflows
   - Caching enabled for faster builds
   - Consistent dependency installation across environments

4. **Performance Benefits**
   - Parallel package downloads
   - Optimized dependency resolution
   - Bytecode compilation for faster startup
   - Efficient caching mechanism

#### 2.2.3. Environment Management
- Development and production environments managed separately
- Virtual environment creation and activation handled automatically
- Consistent package versions across all environments

## 3. Deployment Scenarios

### 3.1. Local Development

```bash
# Using Docker Compose with development target
export DOCKERFILE=Dockerfile.dev
export ENVIRONMENT=development
export DEBUG=true
docker-compose up -d

# Or directly with Docker
docker build -t in-memory-db-service:dev -f backend/Dockerfile.dev .
docker run -d \
  --name in-memory-db-service \
  -p 8000:8000 \
  -e ENVIRONMENT=development \
  -e DEBUG=true \
  in-memory-db-service:dev
```

### 3.2. Production Deployment

```bash
# Using default production settings
docker-compose up -d

# Or directly with Docker
docker build -t in-memory-db-service:prod -f backend/Dockerfile .
docker run -d \
  --name in-memory-db-service \
  -p 8000:8000 \
  -e ENVIRONMENT=production \
  -e DEBUG=false \
  -e WORKERS=4 \
  -e CORS_ORIGINS=http://localhost:8000 \
  in-memory-db-service:prod
```

### 3.3. Environment Variables

The service supports the following environment variables (with defaults):
- `DOCKERFILE`: Dockerfile to use (default: `Dockerfile`)
- `ENVIRONMENT`: Set to either 'development' or 'production' (default: production)
- `DEBUG`: Enable debug mode (default: false)
- `WORKERS`: Number of worker processes (default: 4)
- `CORS_ORIGINS`: Allowed CORS origins (default: http://localhost:8000)
- `PYTHONPATH`: Python path (default: /app)
- `PYTHONUNBUFFERED`: Python output buffering (default: 1)
- `PYTHONDONTWRITEBYTECODE`: Python bytecode generation (default: 1)

### 3.4. Docker Commands

For quick reference, here are all the available Docker commands for managing the service in different environments.

#### 3.4.1. Development Environment

| Command | Description |
|---------|-------------|
| `make docker-build-dev` | Build development Docker image |
| `make docker-run-dev` | Run development container with hot reload |
| `make docker-logs-dev` | Show development container logs |
| `make docker-shell-dev` | Open shell in development container |
| `make docker-test-dev` | Run tests in development container |
| `make docker-stop-dev` | Stop development container |
| `make docker-clean-dev` | Clean development Docker resources |
| `make dev` | Quick start: Build and run development environment |

#### 3.4.2. Production Environment

| Command | Description |
|---------|-------------|
| `make docker-build-prod` | Build production Docker image |
| `make docker-run-prod` | Run production container with resource limits |
| `make docker-logs-prod` | Show production container logs |
| `make docker-shell-prod` | Open shell in production container |
| `make docker-stop-prod` | Stop production container |
| `make docker-clean-prod` | Clean production Docker resources |
| `make prod` | Quick start: Build and run production environment |

#### 3.4.3. Docker Compose Commands

| Command | Description |
|---------|-------------|
| `make compose-up-dev` | Start development environment with Docker Compose |
| `make compose-up-prod` | Start production environment with Docker Compose |
| `make compose-down` | Stop Docker Compose environment |

The project uses a single `docker-compose.yml` file that supports both development and production environments through environment variables:

```bash
# Development mode
make compose-up-dev

# Production mode
make compose-up-prod

# Stop all containers
make compose-down
```

#### 3.4.4. Environment Differences

Key differences between development and production environments:

- **Development:**
  - Uses `Dockerfile.dev`
  - Hot reload enabled
  - Source code mounted as volumes
  - Debug mode enabled
  - Development tools available

- **Production:**
  - Uses `Dockerfile`
  - Resource limits enforced
  - Optimized for performance
  - No source code mounting
  - Multiple workers enabled

## 4. Resource Management

### 4.1. Memory and CPU Limits

The service is configured with the following resource limits in docker-compose.yml:
```yaml
deploy:
  resources:
    limits:
      cpus: '1.0'
      memory: 512M
    reservations:
      cpus: '0.25'
      memory: 256M
```

### 4.2. Monitoring

1. Container Health
   ```bash
   # Check container logs
   docker logs in-memory-db-service
   
   # Monitor resource usage
   docker stats in-memory-db-service
   ```

2. Application Metrics
   - Endpoint response times
   - Memory usage
   - Request/response rates
   - Error rates

## 5. Health Checks

The service includes automated health checks:
```bash
# Check API health
curl http://localhost:8000/api/v1/health

# Health check configuration
interval: 30s
timeout: 5s
retries: 3
start_period: 5s
```

Detailed health check implementation:
- Basic health check endpoint at `/api/v1/utils/health-check`
- Docker health check configuration:
  - 30-second interval
  - 5-second timeout
  - 3 retries
  - 5-second start period

## 6. Logging

Docker logging is configured with:
```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

## 7. Documentation

### 7.1. API Documentation
- Swagger/OpenAPI 3.0 documentation available at `/docs`
- ReDoc alternative documentation at `/redoc`
- Markdown documentation in project repository

### 7.2. Setup Instructions
Detailed setup instructions are available in the sections above. Key documentation includes:
- Docker configuration and build process
- Environment variable configuration
- Resource management
- Health check setup
- Logging configuration

### 7.3. Sample API Calls
API examples are available in the Swagger documentation. Common operations include:
- CRUD operations for resources
- Join operations
- Health checks
- System operations

### 7.4. Troubleshooting Guide
Common issues and solutions:
1. Container fails to start:
   - Check resource limits
   - Verify environment variables
   - Review logs for errors
   
2. Performance issues:
   - Monitor resource usage
   - Check concurrent connections
   - Review logging configuration

3. Health check failures:
   - Verify service connectivity
   - Check resource availability
   - Review health check configuration

## 8. Maintenance

### 8.1. Regular Tasks
   - Monitor resource usage
   - Check for memory leaks
   - Update dependencies
   - Backup data regularly

### 8.2. Updates and Upgrades
   ```bash
   # Pull latest image
   docker pull in-memory-db-service:latest
   
   # Graceful restart
   docker-compose down
   docker-compose up -d
   ```

## 9. Support

For additional support:
1. Check the issue tracker
2. Join our community discussions
3. Contact the maintainers
4. Review the documentation 
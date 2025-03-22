# In-Memory Database Service Makefile

.PHONY: help install test test-normal test-edge lint format clean build run docker-build-dev docker-build-prod docker-run-dev docker-run-prod test-coverage test-verbose test-watch test-performance performance-test performance-benchmark performance-compare test-report docker-stop-dev docker-stop-prod docker-clean-dev docker-clean-prod compose-up-dev compose-up-prod compose-down

# Colors for terminal output
COLOR_RESET=\033[0m
COLOR_BOLD=\033[1m
COLOR_BLUE=\033[34m

help:
	@echo "$(COLOR_BOLD)In-Memory Database Service Management Commands:$(COLOR_RESET)"
	@echo "$(COLOR_BOLD)Development Commands:$(COLOR_RESET)"
	@echo "$(COLOR_BLUE)make install$(COLOR_RESET)      - Install dependencies"
	@echo "$(COLOR_BLUE)make test$(COLOR_RESET)         - Run all tests"
	@echo "$(COLOR_BLUE)make test-normal$(COLOR_RESET)  - Run normal path tests"
	@echo "$(COLOR_BLUE)make test-edge$(COLOR_RESET)    - Run edge case tests"
	@echo "$(COLOR_BLUE)make test-coverage$(COLOR_RESET) - Run tests with coverage report"
	@echo "$(COLOR_BLUE)make test-verbose$(COLOR_RESET) - Run tests with detailed output"
	@echo "$(COLOR_BLUE)make test-watch$(COLOR_RESET)   - Run tests in watch mode"
	@echo "$(COLOR_BLUE)make test-performance$(COLOR_RESET) - Run performance tests with detailed timing"
	@echo "$(COLOR_BLUE)make test-report$(COLOR_RESET)  - Generate comprehensive test report"
	@echo "$(COLOR_BLUE)make lint$(COLOR_RESET)         - Run linter"
	@echo "$(COLOR_BLUE)make format$(COLOR_RESET)       - Format code"
	@echo "$(COLOR_BLUE)make clean$(COLOR_RESET)        - Clean up temporary files"
	@echo "$(COLOR_BLUE)make run$(COLOR_RESET)          - Run the application locally"
	@echo
	@echo "$(COLOR_BOLD)Docker Development Commands:$(COLOR_RESET)"
	@echo "$(COLOR_BLUE)make docker-build-dev$(COLOR_RESET)  - Build development Docker image"
	@echo "$(COLOR_BLUE)make docker-run-dev$(COLOR_RESET)    - Run development Docker container with hot reload"
	@echo "$(COLOR_BLUE)make docker-logs-dev$(COLOR_RESET)   - Show development container logs"
	@echo "$(COLOR_BLUE)make docker-shell-dev$(COLOR_RESET)  - Open shell in development container"
	@echo "$(COLOR_BLUE)make docker-test-dev$(COLOR_RESET)   - Run tests in development container"
	@echo "$(COLOR_BLUE)make docker-stop-dev$(COLOR_RESET)   - Stop development Docker container"
	@echo "$(COLOR_BLUE)make docker-clean-dev$(COLOR_RESET)  - Clean development Docker resources"
	@echo
	@echo "$(COLOR_BOLD)Docker Production Commands:$(COLOR_RESET)"
	@echo "$(COLOR_BLUE)make docker-build-prod$(COLOR_RESET) - Build production Docker image"
	@echo "$(COLOR_BLUE)make docker-run-prod$(COLOR_RESET)   - Run production Docker container"
	@echo "$(COLOR_BLUE)make docker-logs-prod$(COLOR_RESET)   - Show production container logs"
	@echo "$(COLOR_BLUE)make docker-shell-prod$(COLOR_RESET)  - Open shell in production container"
	@echo "$(COLOR_BLUE)make docker-stop-prod$(COLOR_RESET)  - Stop production Docker container"
	@echo "$(COLOR_BLUE)make docker-clean-prod$(COLOR_RESET) - Clean production Docker resources"
	@echo
	@echo "$(COLOR_BOLD)Docker Compose Commands:$(COLOR_RESET)"
	@echo "$(COLOR_BLUE)make compose-up-dev$(COLOR_RESET)  - Start development environment with Docker Compose"
	@echo "$(COLOR_BLUE)make compose-up-prod$(COLOR_RESET) - Start production environment with Docker Compose"
	@echo "$(COLOR_BLUE)make compose-down$(COLOR_RESET)   - Stop Docker Compose environment"

# Development setup
install:
	@echo "Installing dependencies..."
	cd backend && uv sync

# Testing
test:
	@echo "Running all tests..."
	cd backend && pytest -v

# Test Report Generation
test-report:
	@echo "$(COLOR_BOLD)Generating comprehensive test report...$(COLOR_RESET)"
	@cd backend && python tests/generate_test_report.py
	@echo "$(COLOR_BOLD)Test report generation completed.$(COLOR_RESET)"
	@echo "Reports are available in:"
	@echo "- backend/tests/test_reports/ (Markdown report)"
	@echo "- backend/tests/test_reports/coverage.xml (XML coverage)"

# Performance Testing
performance-test:
	@echo "Running all performance tests..."
	cd backend && pytest tests/test_api_performance.py -v

performance-benchmark:
	@echo "Running detailed performance benchmarks..."
	cd backend && pytest tests/test_api_performance.py --benchmark-only --benchmark-save=baseline

performance-compare:
	@echo "Comparing with previous benchmark results..."
	cd backend && pytest tests/test_api_performance.py --benchmark-only --benchmark-compare=baseline

# Code quality
lint:
	@echo "Running linter..."
	cd backend && ./scripts/lint.sh

format:
	@echo "Formatting code..."
	cd backend && ./scripts/format.sh

# Cleanup
clean:
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".eggs" -exec rm -rf {} +
	find . -type d -name ".benchmarks" -exec rm -rf {} +
	find . -type d -name "test_reports" -exec rm -rf {} +

# Application management
build:
	@echo "Building application..."
	cd backend && uv install --editable .

run:
	@echo "Running application..."
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Docker commands for Development
docker-build-dev:
	@echo "$(COLOR_BOLD)Building development Docker image...$(COLOR_RESET)"
	docker build -f ./backend/Dockerfile.dev -t in-memory-db-service:dev ./backend
	@echo "Development image built successfully!"

docker-run-dev:
	@echo "$(COLOR_BOLD)Starting development container with hot reload...$(COLOR_RESET)"
	docker run -d --name in-memory-db-dev -p 8000:8000 \
		-v $(PWD)/backend/app:/app/app \
		-v $(PWD)/backend/tests:/app/tests \
		-v $(PWD)/backend/scripts:/app/scripts \
		-e ENVIRONMENT=development \
		-e DEBUG=true \
		-e PYTHONPATH=/app \
		in-memory-db-service:dev
	@echo "Development container started! API available at http://localhost:8000"
	@echo "View logs with: docker logs -f in-memory-db-dev"

docker-logs-dev:
	@echo "$(COLOR_BOLD)Showing development container logs...$(COLOR_RESET)"
	docker logs -f in-memory-db-dev

docker-shell-dev:
	@echo "$(COLOR_BOLD)Opening shell in development container...$(COLOR_RESET)"
	docker exec -it in-memory-db-dev /bin/bash

docker-test-dev:
	@echo "$(COLOR_BOLD)Running tests in development container...$(COLOR_RESET)"
	docker exec in-memory-db-dev pytest -v

docker-stop-dev:
	@echo "$(COLOR_BOLD)Stopping development Docker container...$(COLOR_RESET)"
	docker stop in-memory-db-dev 2>/dev/null || true
	docker rm in-memory-db-dev 2>/dev/null || true
	@echo "Development container stopped and removed."

docker-clean-dev: docker-stop-dev
	@echo "$(COLOR_BOLD)Cleaning development Docker resources...$(COLOR_RESET)"
	docker rmi in-memory-db-service:dev 2>/dev/null || true
	@echo "Development Docker image removed."

# Docker commands for Production
docker-build-prod:
	@echo "$(COLOR_BOLD)Building production Docker image...$(COLOR_RESET)"
	docker build -f ./backend/Dockerfile -t in-memory-db-service:prod ./backend
	@echo "Production image built successfully!"

docker-run-prod:
	@echo "$(COLOR_BOLD)Starting production container...$(COLOR_RESET)"
	docker run -d --name in-memory-db-prod -p 8000:8000 \
		--memory=512m --cpus=1.0 \
		-e ENVIRONMENT=production \
		-e DEBUG=false \
		-e WORKERS=4 \
		in-memory-db-service:prod
	@echo "Production container started! API available at http://localhost:8000"
	@echo "View logs with: docker logs -f in-memory-db-prod"

docker-logs-prod:
	@echo "$(COLOR_BOLD)Showing production container logs...$(COLOR_RESET)"
	docker logs -f in-memory-db-prod

docker-shell-prod:
	@echo "$(COLOR_BOLD)Opening shell in production container...$(COLOR_RESET)"
	docker exec -it in-memory-db-prod /bin/bash

docker-stop-prod:
	@echo "$(COLOR_BOLD)Stopping production Docker container...$(COLOR_RESET)"
	docker stop in-memory-db-prod 2>/dev/null || true
	docker rm in-memory-db-prod 2>/dev/null || true
	@echo "Production container stopped and removed."

docker-clean-prod: docker-stop-prod
	@echo "$(COLOR_BOLD)Cleaning production Docker resources...$(COLOR_RESET)"
	docker rmi in-memory-db-service:prod 2>/dev/null || true
	@echo "Production Docker image removed."

# Docker Compose commands
compose-up-dev:
	@echo "$(COLOR_BOLD)Starting development environment with Docker Compose...$(COLOR_RESET)"
	DOCKERFILE=Dockerfile.dev ENVIRONMENT=development DEBUG=true docker-compose -f deploy/docker-compose.yml up -d

compose-up-prod:
	@echo "$(COLOR_BOLD)Starting production environment with Docker Compose...$(COLOR_RESET)"
	docker-compose -f deploy/docker-compose.yml up -d

compose-down:
	@echo "$(COLOR_BOLD)Stopping Docker Compose environment...$(COLOR_RESET)"
	docker-compose -f deploy/docker-compose.yml down

# Development workflow shortcuts
dev: docker-build-dev docker-run-dev
prod: docker-build-prod docker-run-prod

# Development workflow shortcuts
dev: install format lint test run 
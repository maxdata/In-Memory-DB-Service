# In-Memory Database Service Makefile

.PHONY: help install test lint format clean build run docker-build docker-run

# Colors for terminal output
COLOR_RESET=\033[0m
COLOR_BOLD=\033[1m
COLOR_BLUE=\033[34m

help:
	@echo "$(COLOR_BOLD)In-Memory Database Service Management Commands:$(COLOR_RESET)"
	@echo "$(COLOR_BLUE)make install$(COLOR_RESET)      - Install dependencies"
	@echo "$(COLOR_BLUE)make test$(COLOR_RESET)         - Run all tests"
	@echo "$(COLOR_BLUE)make lint$(COLOR_RESET)         - Run linter"
	@echo "$(COLOR_BLUE)make format$(COLOR_RESET)       - Format code"
	@echo "$(COLOR_BLUE)make clean$(COLOR_RESET)        - Clean up temporary files"
	@echo "$(COLOR_BLUE)make build$(COLOR_RESET)        - Build the application"
	@echo "$(COLOR_BLUE)make run$(COLOR_RESET)          - Run the application locally"
	@echo "$(COLOR_BLUE)make docker-build$(COLOR_RESET) - Build Docker image"
	@echo "$(COLOR_BLUE)make docker-run$(COLOR_RESET)   - Run Docker container"

# Development setup
install:
	@echo "Installing dependencies..."
	cd backend && uv sync

# Testing
test:
	@echo "Running tests..."
	cd backend && ./scripts/test.sh

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

# Application management
build:
	@echo "Building application..."
	cd backend && uv install --editable .

run:
	@echo "Running application..."
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Docker commands
docker-build:
	@echo "Building Docker image..."
	docker build -t in-memory-db-service ./backend

docker-run:
	@echo "Running Docker container..."
	docker run -p 8000:8000 in-memory-db-service

# Development workflow shortcuts
dev: install format lint test run 
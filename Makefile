# In-Memory Database Service Makefile

.PHONY: help install test test-normal test-edge lint format clean build run docker-build docker-run test-coverage test-verbose test-watch test-performance performance-test performance-benchmark performance-compare test-report

# Colors for terminal output
COLOR_RESET=\033[0m
COLOR_BOLD=\033[1m
COLOR_BLUE=\033[34m

help:
	@echo "$(COLOR_BOLD)In-Memory Database Service Management Commands:$(COLOR_RESET)"
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
	@echo "$(COLOR_BLUE)make build$(COLOR_RESET)        - Build the application"
	@echo "$(COLOR_BLUE)make run$(COLOR_RESET)          - Run the application locally"
	@echo "$(COLOR_BLUE)make docker-build$(COLOR_RESET) - Build Docker image"
	@echo "$(COLOR_BLUE)make docker-run$(COLOR_RESET)   - Run Docker container"
	@echo "$(COLOR_BLUE)make performance-test$(COLOR_RESET) - Run all performance tests"
	@echo "$(COLOR_BLUE)make performance-benchmark$(COLOR_RESET) - Run detailed benchmarks"
	@echo "$(COLOR_BLUE)make performance-compare$(COLOR_RESET) - Compare with previous benchmark"

# Development setup
install:
	@echo "Installing dependencies..."
	cd backend && uv sync

# Testing
test: test-normal test-edge performance-test
	@echo "All tests completed."

test-normal:
	@echo "Running normal path tests..."
	cd backend && pytest tests/test_api_normal.py -v

test-edge:
	@echo "Running edge case tests..."
	cd backend && pytest tests/test_api_edge_cases.py -v

test-coverage:
	@echo "Running tests with coverage..."
	cd backend && pytest tests/ --cov=app --cov-report=term-missing --cov-report=html

test-verbose:
	@echo "Running tests with verbose output..."
	cd backend && pytest tests/ -v --capture=no

test-watch:
	@echo "Running tests in watch mode..."
	cd backend && pytest-watch tests/ -- -v

# Test Report Generation
test-report:
	@echo "$(COLOR_BOLD)Generating comprehensive test report...$(COLOR_RESET)"
	@cd backend && chmod +x tests/generate_test_report.py && ./tests/generate_test_report.py
	@echo "$(COLOR_BOLD)Test report generation completed.$(COLOR_RESET)"
	@echo "Reports are available in backend/tests/test_reports/"

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
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name ".benchmarks" -exec rm -rf {} +
	find . -type d -name "test_reports" -exec rm -rf {} +

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
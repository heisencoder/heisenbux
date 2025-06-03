.PHONY: help test lint format type-check security check-all clean

help:  ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

test:  ## Run tests with coverage
	poetry run pytest --cov=heisenbux --cov-report=xml --cov-report=term-missing

lint:  ## Run ruff linting
	poetry run ruff check .

format:  ## Format code with ruff
	poetry run ruff format .

format-check:  ## Check code formatting without making changes
	poetry run ruff format . --check

type-check:  ## Run mypy type checking
	poetry run mypy .

security:  ## Run security checks with bandit
	poetry run bandit -r heisenbux/

check-all: lint format-check type-check security test  ## Run all checks (CI equivalent)

fix:  ## Auto-fix linting issues and format code
	poetry run ruff check . --fix
	poetry run ruff format .

clean:  ## Clean up generated files
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	rm -rf htmlcov/
	rm -f coverage.xml
	rm -f .coverage
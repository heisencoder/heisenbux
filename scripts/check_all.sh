#!/usr/bin/env bash
# Run all checks similar to GitHub Actions CI

set -e  # Exit on first error

echo "=== Running all checks ==="
echo

echo "1. Checking ruff linting..."
poetry run ruff check .
echo "✓ Linting passed"
echo

echo "2. Checking code formatting..."
poetry run ruff format . --check
echo "✓ Format check passed"
echo

echo "3. Running mypy type checking..."
poetry run mypy .
echo "✓ Type checking passed"
echo

echo "4. Running security checks with bandit..."
poetry run bandit -r heisenbux/
echo "✓ Security checks passed"
echo

echo "5. Running tests with coverage..."
SKIP_INTEGRATION_TESTS=true poetry run pytest --cov=heisenbux --cov-report=xml --cov-report=term-missing
echo "✓ Tests passed"
echo

echo "=== All checks passed! ==="
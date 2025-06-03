# Heisenbux

A Python package for managing investment data and analysis, with support for stocks, ETFs, and other securities.

## Project Structure

```text
heisenbux/
├── heisenbux/           # Source code directory
│   ├── __init__.py     # Package initialization
│   ├── cli.py          # Command-line interface
│   └── download_vanguard.py  # Vanguard fund data downloader
├── tests/              # Test files
├── cache/              # Cached stock data (CSV files)
├── graphs/             # Generated price plots
├── pyproject.toml      # Poetry configuration
├── README.md           # This file
└── .gitignore          # Git ignore rules
```

## Installation

This package uses Poetry for dependency management. To install:

1. Make sure you have Poetry installed:

   ```bash
   pip install poetry
   ```

2. Clone the repository and install dependencies:

   ```bash
   git clone https://github.com/yourusername/heisenbux.git
   cd heisenbux
   poetry install
   ```

## Development

### Running Tests

To run the full test suite with all checks (matching CI):

```bash
# Using taskipy (recommended)
poetry run task check-all

# Using make
make check-all

# Using script
./scripts/check_all.sh
```

To run individual checks:

```bash
# Run tests with coverage
poetry run task test

# Run linting
poetry run task lint

# Check code formatting
poetry run task format-check

# Run type checking
poetry run task type-check

# Run security checks
poetry run task security

# Auto-fix issues and format code
poetry run task fix
```

### Quick Test Commands

```bash
poetry run pytest              # Basic test run
poetry run pytest -xvs         # Stop on first failure, verbose
poetry run pytest -k "test_name"  # Run specific test
```

## License

This project is licensed under the MIT License.

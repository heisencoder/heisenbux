# Heisenbux

A Python package for managing investment data and analysis, with support for stocks, ETFs, and other securities.

## Project Structure

```
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

To run tests:
```bash
poetry run pytest
```

## License

This project is licensed under the MIT License.

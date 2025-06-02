# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Heisenbux is a Python package for fetching and visualizing financial market data using Yahoo Finance. It provides a CLI tool to download historical price data for stocks and ETFs, cache the data locally, and generate price charts.

## Key Architecture

The codebase follows a simple modular architecture:

- **CLI Layer** (`cli.py`): Entry point that handles command-line arguments and orchestrates operations
- **Data Layer** (`finance.py`): Fetches ticker data via yfinance API and manages CSV caching in `cache/` directory
- **Visualization Layer** (`plot.py`): Creates matplotlib plots saved to `graphs/` directory
- **Utility Scripts** (`download_vanguard.py`): Batch operations for popular ETFs

Data flow: CLI → fetch data (with caching) → generate plots → display/save results

## Development Commands

```bash
# Install dependencies
poetry install

# Run the CLI
poetry run heisenbux TICKER              # Download and show plot
poetry run heisenbux TICKER --no-show-plot  # Download without display
poetry run heisenbux TICKER --force-download  # Force fresh download

# Run tests
poetry run pytest

# Linting and formatting
poetry run ruff check .          # Check for issues
poetry run ruff check . --fix    # Auto-fix issues
poetry run ruff format .         # Format code
```

## Important Conventions

- **Python Version**: 3.11+
- **Package Manager**: Poetry
- **Code Style**:
  - Python: Follow the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
  - Python: Ruff with extensive rule set (E, F, I, N, W, B, UP, PL, RUF)
  - Markdown: format with markdownlint, put a blank line after headings and before code blocks
  - All text files: Trim trailing whitespace (enforced via .editorconfig)
- **Line Length**: 88 characters
- **Import Style**: isort-compatible
- **Data Storage**: CSV files in `cache/`, PNG plots in `graphs/`
- **API**: Uses yfinance for market data (365 days historical by default)
- **Typing Annotations**: Add typing annotations to function signatures

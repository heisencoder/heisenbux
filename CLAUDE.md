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

### Claude development methodology

- Do not commit to the git `main` branch. Instead, create and commit to a feature branch.
- Use Convention Commits for git commit messages.
- Each Claude change must have a single purpose.
- After editing code, make sure the linters and tests pass, and then create a git commit to the feature branch.
- If the tests do not pass after 3 attempts, use an alternate strategy. Stop if the alternate strategy fails after 3 more attempts and then ask for help.
- Update markdown files in the same commit as a functional change.
- Both before and after making a functional change, looks for opportunties to perform a pure refactoring to keep the code maintainable. Put the refactoring into a separate Git commit from the functional change.
- After completing requested work, create a GitHub pull request from the feature branch.
- Perform a single code review on GitHub and add comments with suggested changes.
- Resolve any comments in the pull request, if possible, and make sure GitHub Actions pass.
- Use stacked diffs for managing multiple features, via the `git town` subcommand.

### Code quality

- Do not duplicate code or data. Instead, create common libraries or configuration via a refactoring commit.
- Do not use string or numeric literals. Instead, use constants, enums, or similar structures. If a given constant is used in two or more Python modules, then extract this constant into a separate module that only contains constants, enums, and similar configuration.
- Do not duplicate important business logic. Instead, extract this common business logic into helper functions.
- Avoid duplication in tests. Scan tests for similar patterns and create test fixtures and helper functions to encapsulate this duplication.

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
- **Type Annotations**: 
  - Always annotate: Function signatures (parameters and return types), class attributes, module-level variables
  - Sometimes annotate: Empty collections (e.g., `items: list[str] = []`), ambiguous `None` types (e.g., `result: str | None = None`)
  - Rarely annotate: Local variables with obvious types (mypy can infer most local variable types)

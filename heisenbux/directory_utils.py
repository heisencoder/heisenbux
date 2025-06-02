"""Utility functions for heisenbux package."""

from pathlib import Path


def ensure_directory_exists(directory: Path | str) -> Path:
    """Ensure a directory exists, creating it if necessary.

    Args:
        directory: Path to the directory (string or Path object)

    Returns:
        Path object representing the directory
    """
    path = Path(directory) if isinstance(directory, str) else directory
    path.mkdir(parents=True, exist_ok=True)
    return path


def build_file_path(directory: Path | str, ticker: str, suffix: str) -> Path:
    """Build a file path for a given ticker and suffix.

    Args:
        directory: Directory path (string or Path object)
        ticker: Stock ticker symbol
        suffix: File suffix (e.g., '.csv', '_plot.png')

    Returns:
        Complete file path
    """
    dir_path = Path(directory) if isinstance(directory, str) else directory
    return dir_path / f"{ticker.upper()}{suffix}"

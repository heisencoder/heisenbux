"""Helper functions for tests."""

import tempfile
from collections.abc import Generator
from pathlib import Path
from unittest.mock import Mock

import pandas as pd
import pytest

from tests.fixtures.sample_data import create_sample_dataframe


@pytest.fixture
def temp_directory() -> Generator[Path, None, None]:
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


def create_mock_ticker(return_value: pd.DataFrame | None = None) -> Mock:
    """Create a mock yfinance Ticker object.

    Args:
        return_value: DataFrame to return from history() call.
                     If None, uses create_sample_dataframe()

    Returns:
        Mock ticker object with history method configured
    """
    mock_ticker = Mock()
    if return_value is None:
        return_value = create_sample_dataframe()
    mock_ticker.history.return_value = return_value
    return mock_ticker


def assert_valid_dataframe(
    df: pd.DataFrame, expected_columns: list[str], min_rows: int = 1
) -> None:
    """Assert that a DataFrame is valid with expected structure.

    Args:
        df: DataFrame to validate
        expected_columns: List of expected column names
        min_rows: Minimum number of rows expected (default: 1)
    """
    assert df is not None
    assert isinstance(df, pd.DataFrame)
    assert len(df) >= min_rows
    assert all(col in df.columns for col in expected_columns)

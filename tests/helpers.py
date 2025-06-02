"""Helper functions for tests."""

from unittest.mock import Mock

import pandas as pd

from tests.fixtures import sample_data


def create_mock_ticker(dataframe_response: pd.DataFrame | None = None) -> Mock:
    """Create a mock yfinance Ticker object.

    Args:
        dataframe_response: DataFrame to return from history() call.
                           If None, uses create_sample_dataframe()

    Returns:
        Mock ticker object with history method configured
    """
    mock_ticker = Mock()
    if dataframe_response is None:
        dataframe_response = sample_data.create_sample_dataframe()
    mock_ticker.history.return_value = dataframe_response
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

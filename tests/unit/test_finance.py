"""Unit tests for finance module."""

from pathlib import Path
from unittest.mock import Mock, patch

import pandas as pd
import pytest

from heisenbux.constants import (
    ALL_PRICE_COLUMNS,
    CACHE_DIR,
    CLOSE_COLUMN,
    CSV_EXTENSION,
)
from heisenbux.finance import get_ticker_data
from tests.constants import TEST_DATE_2020, TEST_PERIODS
from tests.fixtures.sample_data import SAMPLE_TICKER
from tests.helpers import assert_valid_dataframe, create_mock_ticker


class TestGetTickerData:
    """Test cases for get_ticker_data function."""

    @pytest.fixture
    def mock_yfinance(self):
        """Create a mock yfinance Ticker object."""
        return create_mock_ticker()

    def test_get_ticker_data_downloads_fresh_data(
        self, mock_yfinance, temp_directory: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that get_ticker_data downloads fresh data when cache doesn't exist."""
        monkeypatch.chdir(temp_directory)

        with patch("yfinance.Ticker", return_value=mock_yfinance):
            df = get_ticker_data(SAMPLE_TICKER)

        assert_valid_dataframe(df, ALL_PRICE_COLUMNS)

        # Check that cache file was created
        cache_file = temp_directory / CACHE_DIR / f"{SAMPLE_TICKER}{CSV_EXTENSION}"
        assert cache_file.exists()

    def test_get_ticker_data_uses_cache(
        self, temp_directory: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that get_ticker_data uses cached data when available."""
        monkeypatch.chdir(temp_directory)

        # Create cache directory and file
        cache_dir = temp_directory / CACHE_DIR
        cache_dir.mkdir()
        cache_file = cache_dir / f"{SAMPLE_TICKER}{CSV_EXTENSION}"

        # Save sample data to cache
        from tests.fixtures.sample_data import create_sample_dataframe

        sample_df = create_sample_dataframe()
        sample_df.to_csv(cache_file)

        # Mock yfinance to ensure it's not called
        with patch("yfinance.Ticker") as mock_ticker:
            df = get_ticker_data(SAMPLE_TICKER)

        mock_ticker.assert_not_called()
        assert_valid_dataframe(df, ALL_PRICE_COLUMNS, min_rows=len(sample_df))

    def test_get_ticker_data_force_download(
        self, mock_yfinance, temp_directory: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that force_download bypasses cache."""
        monkeypatch.chdir(temp_directory)

        # Create cache directory and file
        cache_dir = temp_directory / CACHE_DIR
        cache_dir.mkdir()
        cache_file = cache_dir / f"{SAMPLE_TICKER}{CSV_EXTENSION}"

        # Save old data to cache
        old_df = pd.DataFrame(
            {CLOSE_COLUMN: [1, 2, 3]},
            index=pd.date_range(TEST_DATE_2020, periods=TEST_PERIODS),
        )
        old_df.to_csv(cache_file)

        with patch("yfinance.Ticker", return_value=mock_yfinance):
            df = get_ticker_data(SAMPLE_TICKER, force_download=True)

        assert_valid_dataframe(df, ALL_PRICE_COLUMNS, min_rows=TEST_PERIODS + 1)

    def test_get_ticker_data_handles_download_error(
        self, temp_directory: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that get_ticker_data propagates download errors."""
        monkeypatch.chdir(temp_directory)

        mock_ticker = Mock()
        mock_ticker.history.side_effect = RuntimeError("Network error")

        with patch("yfinance.Ticker", return_value=mock_ticker):
            with pytest.raises(RuntimeError, match="Network error"):
                get_ticker_data(SAMPLE_TICKER)

    def test_get_ticker_data_handles_empty_response(
        self, temp_directory: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that get_ticker_data raises ValueError for empty responses."""
        monkeypatch.chdir(temp_directory)

        mock_ticker = Mock()
        mock_ticker.history.return_value = pd.DataFrame()

        with patch("yfinance.Ticker", return_value=mock_ticker):
            with pytest.raises(ValueError, match="No data found for ticker"):
                get_ticker_data(SAMPLE_TICKER)

"""Unit tests for finance module."""

from pathlib import Path
from unittest.mock import Mock, patch

import pandas as pd
import pytest

from heisenbux import constants, finance
from tests import constants as test_constants
from tests import helpers
from tests.fixtures import sample_data


class TestGetTickerData:
    """Test cases for get_ticker_data function."""

    @pytest.fixture
    def mock_yfinance(self) -> Mock:
        """Create a mock yfinance Ticker object."""
        return helpers.create_mock_ticker()

    def test_get_ticker_data_downloads_fresh_data(
        self, mock_yfinance: Mock, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that get_ticker_data downloads fresh data when cache doesn't exist."""
        monkeypatch.chdir(tmp_path)

        with patch("yfinance.Ticker", return_value=mock_yfinance):
            df = finance.get_ticker_data(sample_data.SAMPLE_TICKER)

        helpers.assert_valid_dataframe(df, constants.ALL_PRICE_COLUMNS)

        # Check that cache file was created
        cache_file = (
            tmp_path
            / constants.Directories.CACHE
            / f"{sample_data.SAMPLE_TICKER}{constants.FileExtensions.CSV}"
        )
        assert cache_file.exists()

    def test_get_ticker_data_uses_cache(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that get_ticker_data uses cached data when available."""
        monkeypatch.chdir(tmp_path)

        # Create cache directory and file
        cache_dir = tmp_path / constants.Directories.CACHE
        cache_dir.mkdir()
        cache_file = (
            cache_dir / f"{sample_data.SAMPLE_TICKER}{constants.FileExtensions.CSV}"
        )

        # Save sample data to cache
        sample_df = sample_data.create_sample_dataframe()
        sample_df.to_csv(cache_file)

        # Mock yfinance to ensure it's not called
        with patch("yfinance.Ticker") as mock_ticker:
            df = finance.get_ticker_data(sample_data.SAMPLE_TICKER)

        mock_ticker.assert_not_called()
        helpers.assert_valid_dataframe(
            df, constants.ALL_PRICE_COLUMNS, min_rows=len(sample_df)
        )

    def test_get_ticker_data_force_download(
        self, mock_yfinance: Mock, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that force_download bypasses cache."""
        monkeypatch.chdir(tmp_path)

        # Create cache directory and file
        cache_dir = tmp_path / constants.Directories.CACHE
        cache_dir.mkdir()
        cache_file = (
            cache_dir / f"{sample_data.SAMPLE_TICKER}{constants.FileExtensions.CSV}"
        )

        # Save old data to cache
        old_df = pd.DataFrame(
            {constants.DataFrameColumns.CLOSE: [1, 2, 3]},
            index=pd.date_range(
                test_constants.TEST_DATE_2020, periods=test_constants.TEST_PERIODS
            ),
        )
        old_df.to_csv(cache_file)

        with patch("yfinance.Ticker", return_value=mock_yfinance):
            df = finance.get_ticker_data(sample_data.SAMPLE_TICKER, force_download=True)

        helpers.assert_valid_dataframe(
            df, constants.ALL_PRICE_COLUMNS, min_rows=test_constants.TEST_PERIODS + 1
        )

    def test_get_ticker_data_handles_download_error(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that get_ticker_data propagates download errors."""
        monkeypatch.chdir(tmp_path)

        mock_ticker = Mock()
        mock_ticker.history.side_effect = RuntimeError("Network error")

        with patch("yfinance.Ticker", return_value=mock_ticker):
            with pytest.raises(RuntimeError, match="Network error"):
                finance.get_ticker_data(sample_data.SAMPLE_TICKER)

    def test_get_ticker_data_handles_empty_response(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that get_ticker_data raises ValueError for empty responses."""
        monkeypatch.chdir(tmp_path)

        mock_ticker = Mock()
        mock_ticker.history.return_value = pd.DataFrame()

        with patch("yfinance.Ticker", return_value=mock_ticker):
            with pytest.raises(ValueError, match="No data found for ticker"):
                finance.get_ticker_data(sample_data.SAMPLE_TICKER)

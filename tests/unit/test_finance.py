"""Unit tests for finance module."""

import tempfile
from collections.abc import Generator
from pathlib import Path
from unittest.mock import Mock, patch

import pandas as pd
import pytest

from heisenbux.finance import get_ticker_data
from tests.fixtures.sample_data import SAMPLE_TICKER, create_sample_dataframe


class TestGetTickerData:
    """Test cases for get_ticker_data function."""

    @pytest.fixture
    def mock_yfinance(self) -> Mock:
        """Create a mock yfinance Ticker object."""
        mock_ticker = Mock()
        mock_ticker.history.return_value = create_sample_dataframe()
        return mock_ticker

    @pytest.fixture
    def temp_cache_dir(self) -> Generator[Path, None, None]:
        """Create a temporary cache directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    def test_get_ticker_data_downloads_fresh_data(
        self, mock_yfinance: Mock, temp_cache_dir: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that get_ticker_data downloads fresh data when cache doesn't exist."""
        monkeypatch.chdir(temp_cache_dir)

        with patch("yfinance.Ticker", return_value=mock_yfinance):
            df = get_ticker_data(SAMPLE_TICKER)

        assert df is not None
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert all(
            col in df.columns for col in ["Open", "High", "Low", "Close", "Volume"]
        )

        # Check that cache file was created
        cache_file = temp_cache_dir / "cache" / f"{SAMPLE_TICKER}.csv"
        assert cache_file.exists()

    def test_get_ticker_data_uses_cache(
        self, temp_cache_dir: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that get_ticker_data uses cached data when available."""
        monkeypatch.chdir(temp_cache_dir)

        # Create cache directory and file
        cache_dir = temp_cache_dir / "cache"
        cache_dir.mkdir()
        cache_file = cache_dir / f"{SAMPLE_TICKER}.csv"

        # Save sample data to cache
        sample_df = create_sample_dataframe()
        sample_df.to_csv(cache_file)

        # Mock yfinance to ensure it's not called
        with patch("yfinance.Ticker") as mock_ticker:
            df = get_ticker_data(SAMPLE_TICKER)

        mock_ticker.assert_not_called()
        assert df is not None
        assert isinstance(df, pd.DataFrame)
        assert len(df) == len(sample_df)

    def test_get_ticker_data_force_download(
        self, mock_yfinance: Mock, temp_cache_dir: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that force_download bypasses cache."""
        monkeypatch.chdir(temp_cache_dir)

        # Create cache directory and file
        cache_dir = temp_cache_dir / "cache"
        cache_dir.mkdir()
        cache_file = cache_dir / f"{SAMPLE_TICKER}.csv"

        # Save old data to cache
        old_df = pd.DataFrame(
            {"Close": [1, 2, 3]}, index=pd.date_range("2020-01-01", periods=3)
        )
        old_df.to_csv(cache_file)

        with patch("yfinance.Ticker", return_value=mock_yfinance):
            df = get_ticker_data(SAMPLE_TICKER, force_download=True)

        assert df is not None
        # New data should have more rows than old cached data
        min_expected_rows = 3
        assert len(df) > min_expected_rows

    def test_get_ticker_data_handles_download_error(
        self, temp_cache_dir: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that get_ticker_data handles download errors gracefully."""
        monkeypatch.chdir(temp_cache_dir)

        mock_ticker = Mock()
        mock_ticker.history.side_effect = Exception("Network error")

        with patch("yfinance.Ticker", return_value=mock_ticker):
            df = get_ticker_data(SAMPLE_TICKER)

        assert df is None

    def test_get_ticker_data_handles_empty_response(
        self, temp_cache_dir: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that get_ticker_data handles empty responses."""
        monkeypatch.chdir(temp_cache_dir)

        mock_ticker = Mock()
        mock_ticker.history.return_value = pd.DataFrame()

        with patch("yfinance.Ticker", return_value=mock_ticker):
            df = get_ticker_data(SAMPLE_TICKER)

        assert df is None

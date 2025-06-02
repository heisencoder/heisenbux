"""Integration tests for data sources."""

import os
from pathlib import Path
from unittest.mock import patch

import pandas as pd
import pytest

from heisenbux.finance import get_ticker_data
from tests.fixtures.sample_data import create_sample_dataframe


class TestDataSourceIntegration:
    """Integration tests for external data sources."""

    @pytest.mark.skipif(
        os.environ.get("SKIP_INTEGRATION_TESTS", "true").lower() == "true",
        reason="Skipping integration tests",
    )
    def test_real_yfinance_download(self) -> None:
        """Test actual download from yfinance (requires internet)."""
        # Use a well-known ticker that should always exist
        df = get_ticker_data("AAPL", force_download=True)

        assert df is not None
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert all(
            col in df.columns for col in ["Open", "High", "Low", "Close", "Volume"]
        )

    def test_mock_yfinance_integration(self) -> None:
        """Test integration with mocked yfinance responses."""
        with patch("yfinance.Ticker") as mock_ticker_class:
            # Create a mock ticker instance
            mock_ticker = mock_ticker_class.return_value
            mock_ticker.history.return_value = create_sample_dataframe()

            df = get_ticker_data("TEST", force_download=True)

            assert df is not None
            assert isinstance(df, pd.DataFrame)
            assert len(df) > 0

    def test_error_handling_integration(self) -> None:
        """Test error handling in integration scenarios."""
        with patch("yfinance.Ticker") as mock_ticker_class:
            # Simulate network error
            mock_ticker = mock_ticker_class.return_value
            mock_ticker.history.side_effect = ConnectionError("Network error")

            df = get_ticker_data("TEST", force_download=True)

            assert df is None

    def test_cache_integration(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test cache integration with file system."""
        monkeypatch.chdir(tmp_path)
        with patch("yfinance.Ticker") as mock_ticker_class:
            mock_ticker = mock_ticker_class.return_value
            mock_ticker.history.return_value = create_sample_dataframe()

            # First call should download
            df1 = get_ticker_data("TEST")
            assert df1 is not None

            # Second call should use cache
            mock_ticker.history.reset_mock()
            df2 = get_ticker_data("TEST")
            assert df2 is not None
            mock_ticker.history.assert_not_called()

            # Force download should bypass cache
            df3 = get_ticker_data("TEST", force_download=True)
            assert df3 is not None
            mock_ticker.history.assert_called_once()

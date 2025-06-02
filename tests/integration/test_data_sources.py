"""Integration tests for data sources."""

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from heisenbux.constants import ALL_PRICE_COLUMNS
from heisenbux.finance import get_ticker_data
from tests.constants import SKIP_INTEGRATION_ENV_VAR, TEST_TICKER_AAPL, TEST_TICKER_TEST
from tests.helpers import assert_valid_dataframe, create_mock_ticker


class TestDataSourceIntegration:
    """Integration tests for external data sources."""

    @pytest.mark.skipif(
        os.environ.get(SKIP_INTEGRATION_ENV_VAR, "true").lower() == "true",
        reason="Skipping integration tests",
    )
    def test_real_yfinance_download(self) -> None:
        """Test actual download from yfinance (requires internet)."""
        # Use a well-known ticker that should always exist
        df = get_ticker_data(TEST_TICKER_AAPL, force_download=True)

        assert_valid_dataframe(df, ALL_PRICE_COLUMNS)

    def test_mock_yfinance_integration(self) -> None:
        """Test integration with mocked yfinance responses."""
        with patch("yfinance.Ticker") as mock_ticker_class:
            # Create a mock ticker instance
            mock_ticker_class.return_value = create_mock_ticker()

            df = get_ticker_data(TEST_TICKER_TEST, force_download=True)

            assert_valid_dataframe(df, ALL_PRICE_COLUMNS)

    def test_error_handling_integration(self) -> None:
        """Test error handling in integration scenarios."""
        with patch("yfinance.Ticker") as mock_ticker_class:
            # Simulate network error
            mock_ticker = create_mock_ticker()
            mock_ticker.history.side_effect = ConnectionError("Network error")
            mock_ticker_class.return_value = mock_ticker

            with pytest.raises(ConnectionError, match="Network error"):
                get_ticker_data(TEST_TICKER_TEST, force_download=True)

    def test_cache_integration(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test cache integration with file system."""
        monkeypatch.chdir(tmp_path)
        with patch("yfinance.Ticker") as mock_ticker_class:
            mock_ticker = create_mock_ticker()
            mock_ticker_class.return_value = mock_ticker

            # First call should download
            df1 = get_ticker_data(TEST_TICKER_TEST)
            assert df1 is not None

            # Second call should use cache
            mock_ticker.history.reset_mock()
            df2 = get_ticker_data(TEST_TICKER_TEST)
            assert df2 is not None
            mock_ticker.history.assert_not_called()

            # Force download should bypass cache
            df3 = get_ticker_data(TEST_TICKER_TEST, force_download=True)
            assert df3 is not None
            mock_ticker.history.assert_called_once()

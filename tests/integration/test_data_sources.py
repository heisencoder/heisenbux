"""Integration tests for data sources."""

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from heisenbux import constants, finance
from tests import constants as test_constants
from tests import helpers


class TestDataSourceIntegration:
    """Integration tests for external data sources."""

    @pytest.mark.skipif(
        os.environ.get(test_constants.SKIP_INTEGRATION_ENV_VAR, "true").lower()
        == "true",
        reason="Skipping integration tests",
    )
    def test_real_yfinance_download(self) -> None:
        """Test actual download from yfinance (requires internet)."""
        # Use a well-known ticker that should always exist
        df = finance.get_ticker_data(
            test_constants.TestTickers.AAPL, force_download=True
        )

        helpers.assert_valid_dataframe(df, constants.ALL_PRICE_COLUMNS)

    def test_mock_yfinance_integration(self) -> None:
        """Test integration with mocked yfinance responses."""
        with patch("yfinance.Ticker") as mock_ticker_class:
            # Create a mock ticker instance
            mock_ticker_class.return_value = helpers.create_mock_ticker()

            df = finance.get_ticker_data(
                test_constants.TestTickers.TEST, force_download=True
            )

            helpers.assert_valid_dataframe(df, constants.ALL_PRICE_COLUMNS)

    def test_error_handling_integration(self) -> None:
        """Test error handling in integration scenarios."""
        with patch("yfinance.Ticker") as mock_ticker_class:
            # Simulate network error
            mock_ticker = helpers.create_mock_ticker()
            mock_ticker.history.side_effect = ConnectionError("Network error")
            mock_ticker_class.return_value = mock_ticker

            with pytest.raises(ConnectionError, match="Network error"):
                finance.get_ticker_data(
                    test_constants.TestTickers.TEST, force_download=True
                )

    def test_cache_integration(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test cache integration with file system."""
        monkeypatch.chdir(tmp_path)
        with patch("yfinance.Ticker") as mock_ticker_class:
            mock_ticker = helpers.create_mock_ticker()
            mock_ticker_class.return_value = mock_ticker

            # First call should download
            df1 = finance.get_ticker_data(test_constants.TestTickers.TEST)
            assert df1 is not None

            # Second call should use cache
            mock_ticker.history.reset_mock()
            df2 = finance.get_ticker_data(test_constants.TestTickers.TEST)
            assert df2 is not None
            mock_ticker.history.assert_not_called()

            # Force download should bypass cache
            df3 = finance.get_ticker_data(
                test_constants.TestTickers.TEST, force_download=True
            )
            assert df3 is not None
            mock_ticker.history.assert_called_once()

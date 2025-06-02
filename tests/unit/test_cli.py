"""Unit tests for CLI module."""

from unittest.mock import Mock, patch

import pandas as pd
import pytest
from click.testing import CliRunner

from heisenbux.cli import main
from tests.fixtures.sample_data import SAMPLE_TICKER, create_sample_dataframe


class TestCLI:
    """Test cases for CLI commands."""

    @pytest.fixture
    def runner(self) -> CliRunner:
        """Create a Click test runner."""
        return CliRunner()

    @pytest.fixture
    def mock_data(self) -> pd.DataFrame:
        """Get mock data for testing."""
        return create_sample_dataframe()

    @patch("heisenbux.plot.save_plot")
    @patch("heisenbux.finance.get_ticker_data")
    def test_cli_downloads_and_plots_ticker(
        self,
        mock_get_ticker: Mock,
        mock_plot: Mock,
        runner: CliRunner,
        mock_data: pd.DataFrame,
    ) -> None:
        """Test that CLI downloads data and creates plot."""
        mock_get_ticker.return_value = mock_data

        result = runner.invoke(main, [SAMPLE_TICKER])

        assert result.exit_code == 0

        mock_get_ticker.assert_called_once_with(SAMPLE_TICKER, False)
        mock_plot.assert_called_once_with(mock_data, SAMPLE_TICKER)

    @patch("heisenbux.plot.save_plot")
    @patch("heisenbux.finance.get_ticker_data")
    def test_cli_no_show_plot_option(
        self,
        mock_get_ticker: Mock,
        mock_plot: Mock,
        runner: CliRunner,
        mock_data: pd.DataFrame,
    ) -> None:
        """Test that --no-show-plot option works correctly."""
        mock_get_ticker.return_value = mock_data

        result = runner.invoke(main, [SAMPLE_TICKER, "--no-show-plot"])

        assert result.exit_code == 0
        mock_plot.assert_not_called()

    @patch("heisenbux.plot.save_plot")
    @patch("heisenbux.finance.get_ticker_data")
    def test_cli_force_download_option(
        self,
        mock_get_ticker: Mock,
        mock_plot: Mock,
        runner: CliRunner,
        mock_data: pd.DataFrame,
    ) -> None:
        """Test that --force-download option works correctly."""
        mock_get_ticker.return_value = mock_data

        result = runner.invoke(main, [SAMPLE_TICKER, "--force-download"])

        assert result.exit_code == 0
        mock_get_ticker.assert_called_once_with(SAMPLE_TICKER, True)

    @patch("heisenbux.finance.get_ticker_data")
    def test_cli_handles_download_failure(
        self, mock_get_ticker: Mock, runner: CliRunner
    ) -> None:
        """Test that CLI handles download failures gracefully."""
        mock_get_ticker.side_effect = ValueError("No data found for ticker TEST")

        result = runner.invoke(main, [SAMPLE_TICKER])

        assert result.exit_code == 1  # CLI returns 1 on Abort
        assert "Error: No data found for ticker TEST" in result.output

    def test_cli_requires_ticker_argument(self, runner: CliRunner) -> None:
        """Test that CLI requires a ticker argument."""
        result = runner.invoke(main, [])

        # Click returns exit code 2 for missing required arguments
        missing_argument_exit_code = 2
        assert result.exit_code == missing_argument_exit_code
        assert "Missing argument 'TICKER'" in result.output

    @patch("heisenbux.plot.save_plot")
    @patch("heisenbux.finance.get_ticker_data")
    def test_cli_converts_ticker_to_uppercase(
        self,
        mock_get_ticker: Mock,
        mock_plot: Mock,
        runner: CliRunner,
        mock_data: pd.DataFrame,
    ) -> None:
        """Test that CLI converts ticker to uppercase."""
        mock_get_ticker.return_value = mock_data

        result = runner.invoke(main, ["aapl"])

        assert result.exit_code == 0
        mock_get_ticker.assert_called_once_with("aapl", False)
        mock_plot.assert_called_once_with(mock_data, "aapl")

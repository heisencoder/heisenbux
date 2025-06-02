"""Unit tests for CLI module."""

from unittest.mock import Mock, patch

import pandas as pd
import pytest
from click.testing import CliRunner

from heisenbux import cli, constants
from tests import constants as test_constants
from tests.fixtures import sample_data


class TestCLI:
    """Test cases for CLI commands."""

    @pytest.fixture
    def runner(self) -> CliRunner:
        """Create a Click test runner."""
        return CliRunner()

    @pytest.fixture
    def mock_data(self) -> pd.DataFrame:
        """Get mock data for testing."""
        return sample_data.create_sample_dataframe()

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

        result = runner.invoke(cli.main, [sample_data.SAMPLE_TICKER])

        assert result.exit_code == 0

        mock_get_ticker.assert_called_once_with(sample_data.SAMPLE_TICKER, False)
        mock_plot.assert_called_once_with(mock_data, sample_data.SAMPLE_TICKER)

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

        result = runner.invoke(cli.main, [sample_data.SAMPLE_TICKER, "--no-show-plot"])

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

        result = runner.invoke(
            cli.main, [sample_data.SAMPLE_TICKER, "--force-download"]
        )

        assert result.exit_code == 0
        mock_get_ticker.assert_called_once_with(sample_data.SAMPLE_TICKER, True)

    @patch("heisenbux.finance.get_ticker_data")
    def test_cli_handles_download_failure(
        self, mock_get_ticker: Mock, runner: CliRunner
    ) -> None:
        """Test that CLI handles download failures gracefully."""
        mock_get_ticker.side_effect = ValueError("No data found for ticker TEST")

        result = runner.invoke(cli.main, [sample_data.SAMPLE_TICKER])

        assert result.exit_code == constants.EXIT_ERROR  # CLI returns 1 on Abort
        assert (
            f"{test_constants.TestErrorMessages.ERROR_PREFIX}"
            "No data found for ticker TEST"
            in result.output
        )

    def test_cli_requires_ticker_argument(self, runner: CliRunner) -> None:
        """Test that CLI requires a ticker argument."""
        result = runner.invoke(cli.main, [])

        # Click returns exit code 2 for missing required arguments
        assert result.exit_code == constants.EXIT_USAGE_ERROR
        assert test_constants.TestErrorMessages.MISSING_TICKER in result.output

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

        result = runner.invoke(cli.main, [test_constants.TestTickers.AAPL_LOWER])

        assert result.exit_code == 0
        mock_get_ticker.assert_called_once_with(
            test_constants.TestTickers.AAPL_LOWER, False
        )
        mock_plot.assert_called_once_with(
            mock_data, test_constants.TestTickers.AAPL_LOWER
        )

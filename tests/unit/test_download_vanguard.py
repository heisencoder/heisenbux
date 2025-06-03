"""Unit tests for download_vanguard module."""

from unittest.mock import Mock, patch

import click

from heisenbux import download_vanguard
from tests.fixtures import sample_data


class TestDownloadVanguardFunds:
    """Test cases for download_vanguard functions."""

    @patch("heisenbux.download_vanguard._run_heisenbux_for_ticker")
    def test_download_funds(self, mock_run: Mock) -> None:
        """Test that download_funds calls the heisenbux function for each fund."""
        download_vanguard.download_funds(sample_data.VANGUARD_TEST_FUNDS)

        # Check that the function was called for each fund
        assert mock_run.call_count == len(sample_data.VANGUARD_TEST_FUNDS)

        # Check the calls were made with correct arguments
        for fund in sample_data.VANGUARD_TEST_FUNDS:
            mock_run.assert_any_call(fund, show_plot=False, force_download=False)

    @patch("heisenbux.download_vanguard._run_heisenbux_for_ticker")
    def test_generate_plots(self, mock_run: Mock) -> None:
        """Test that generate_plots calls the heisenbux function for each fund."""
        download_vanguard.generate_plots(sample_data.VANGUARD_TEST_FUNDS)

        # Check that the function was called for each fund
        assert mock_run.call_count == len(sample_data.VANGUARD_TEST_FUNDS)

        # Check the calls were made with correct arguments
        for fund in sample_data.VANGUARD_TEST_FUNDS:
            mock_run.assert_any_call(fund, show_plot=True, force_download=False)

    @patch("heisenbux.download_vanguard._run_heisenbux_for_ticker")
    @patch("builtins.print")
    def test_download_funds_prints_progress(
        self, mock_print: Mock, mock_run: Mock
    ) -> None:
        """Test that download_funds prints progress messages."""
        download_vanguard.download_funds(["VTI"])

        # Check that progress message was printed
        mock_print.assert_called_with("\nDownloading data for VTI...")

    @patch("heisenbux.download_vanguard._run_heisenbux_for_ticker")
    @patch("builtins.print")
    def test_generate_plots_prints_progress(
        self, mock_print: Mock, mock_run: Mock
    ) -> None:
        """Test that generate_plots prints progress messages."""
        download_vanguard.generate_plots(["VTI"])

        # Check that progress message was printed
        mock_print.assert_called_with("\nGenerating plot for VTI...")

    @patch("heisenbux.cli.main")
    def test_run_heisenbux_for_ticker_failure(self, mock_main: Mock) -> None:
        """Test that CLI failures are handled gracefully."""
        mock_main.side_effect = click.Abort()

        # The function should handle the exception gracefully
        download_vanguard._run_heisenbux_for_ticker(
            "VTI", show_plot=False, force_download=False
        )

        # The main function should have been called
        mock_main.assert_called_once_with(standalone_mode=False)

"""Unit tests for download_vanguard module."""

import subprocess
from unittest.mock import Mock, call, patch

import pytest

from heisenbux.constants import (
    NO_FORCE_DOWNLOAD_FLAG,
    NO_SHOW_PLOT_FLAG,
    POETRY_RUN_HEISENBUX,
    SHOW_PLOT_FLAG,
)
from heisenbux.download_vanguard import download_funds, generate_plots
from tests.fixtures.sample_data import VANGUARD_TEST_FUNDS


class TestDownloadVanguardFunds:
    """Test cases for download_vanguard functions."""

    @patch("heisenbux.download_vanguard.subprocess.run")
    def test_download_funds(self, mock_run: Mock) -> None:
        """Test that download_funds calls subprocess for each fund."""
        download_funds(VANGUARD_TEST_FUNDS)

        # Check that subprocess was called for each fund
        assert mock_run.call_count == len(VANGUARD_TEST_FUNDS)

        # Check the calls were made with correct arguments
        expected_calls = [
            call([*POETRY_RUN_HEISENBUX, fund, NO_SHOW_PLOT_FLAG], check=True)
            for fund in VANGUARD_TEST_FUNDS
        ]
        mock_run.assert_has_calls(expected_calls, any_order=False)

    @patch("heisenbux.download_vanguard.subprocess.run")
    def test_generate_plots(self, mock_run: Mock) -> None:
        """Test that generate_plots calls subprocess for each fund."""
        generate_plots(VANGUARD_TEST_FUNDS)

        # Check that subprocess was called for each fund
        assert mock_run.call_count == len(VANGUARD_TEST_FUNDS)

        # Check the calls were made with correct arguments
        expected_calls = [
            call(
                [*POETRY_RUN_HEISENBUX, fund, NO_FORCE_DOWNLOAD_FLAG, SHOW_PLOT_FLAG],
                check=True,
            )
            for fund in VANGUARD_TEST_FUNDS
        ]
        mock_run.assert_has_calls(expected_calls, any_order=False)

    @patch("heisenbux.download_vanguard.subprocess.run")
    @patch("builtins.print")
    def test_download_funds_prints_progress(
        self, mock_print: Mock, mock_run: Mock
    ) -> None:
        """Test that download_funds prints progress messages."""
        download_funds(["VTI"])

        # Check that progress message was printed
        mock_print.assert_called_with("\nDownloading data for VTI...")

    @patch("heisenbux.download_vanguard.subprocess.run")
    @patch("builtins.print")
    def test_generate_plots_prints_progress(
        self, mock_print: Mock, mock_run: Mock
    ) -> None:
        """Test that generate_plots prints progress messages."""
        generate_plots(["VTI"])

        # Check that progress message was printed
        mock_print.assert_called_with("\nGenerating plot for VTI...")

    @patch("heisenbux.download_vanguard.subprocess.run")
    def test_subprocess_failure_propagates(self, mock_run: Mock) -> None:
        """Test that subprocess failures are propagated."""
        mock_run.side_effect = subprocess.CalledProcessError(1, "heisenbux")

        # The function should raise the exception
        with pytest.raises(subprocess.CalledProcessError):
            download_funds(["VTI"])

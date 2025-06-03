"""Unit tests for plot module."""

from pathlib import Path
from unittest.mock import Mock, patch

import pandas as pd
import pytest

from heisenbux import constants, plot
from tests.fixtures import sample_data


class TestSavePlot:
    """Test cases for save_plot function."""

    @pytest.fixture
    def sample_df(self) -> pd.DataFrame:
        """Get sample DataFrame for testing."""
        return sample_data.create_sample_dataframe()

    @patch("matplotlib.pyplot.savefig")
    @patch("matplotlib.pyplot.show")
    def test_save_plot_saves_file(  # noqa: PLR0913
        self,
        mock_show: Mock,
        mock_savefig: Mock,
        sample_df: pd.DataFrame,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test that save_plot saves the plot file."""
        monkeypatch.chdir(tmp_path)

        plot.save_plot(sample_df, sample_data.SAMPLE_TICKER)

        # Check that savefig was called
        mock_savefig.assert_called_once()
        save_args = mock_savefig.call_args[0]
        expected_path = (
            Path(constants.Directories.GRAPHS)
            / f"{sample_data.SAMPLE_TICKER}{constants.PLOT_SUFFIX}"
        )
        assert save_args[0] == expected_path

        # Check that show was called
        mock_show.assert_called_once()

    @patch("matplotlib.pyplot.savefig")
    def test_save_plot_creates_graphs_directory(
        self,
        mock_savefig: Mock,
        sample_df: pd.DataFrame,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test that save_plot creates graphs directory if it doesn't exist."""
        monkeypatch.chdir(tmp_path)

        graphs_dir = Path(constants.Directories.GRAPHS)
        assert not graphs_dir.exists()

        with patch("matplotlib.pyplot.show"):
            plot.save_plot(sample_df, sample_data.SAMPLE_TICKER)

        assert graphs_dir.exists()
        assert graphs_dir.is_dir()

    @patch("matplotlib.pyplot.figure")
    @patch("matplotlib.pyplot.show")
    @patch("matplotlib.pyplot.savefig")
    def test_save_plot_creates_correct_plot(  # noqa: PLR0913
        self,
        mock_savefig: Mock,
        mock_show: Mock,
        mock_figure: Mock,
        sample_df: pd.DataFrame,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test that save_plot creates a plot with correct properties."""
        monkeypatch.chdir(tmp_path)

        # Let other pyplot functions work normally
        with (
            patch("matplotlib.pyplot.plot") as mock_plot,
            patch("matplotlib.pyplot.title") as mock_title,
            patch("matplotlib.pyplot.xlabel") as mock_xlabel,
            patch("matplotlib.pyplot.ylabel") as mock_ylabel,
            patch("matplotlib.pyplot.grid") as mock_grid,
            patch("matplotlib.pyplot.legend") as mock_legend,
            patch("matplotlib.pyplot.xticks") as mock_xticks,
            patch("matplotlib.pyplot.tight_layout") as mock_tight_layout,
        ):
            plot.save_plot(sample_df, sample_data.SAMPLE_TICKER)

        # Check that figure was created with correct size
        mock_figure.assert_called_once_with(figsize=constants.FIGURE_SIZE)

        # Check that plot was called with correct data
        mock_plot.assert_called_once()
        plot_args = mock_plot.call_args[0]
        assert len(plot_args[0]) == len(sample_df)  # x data (dates)
        assert len(plot_args[1]) == len(sample_df)  # y data (close prices)

        # Check labels and title
        mock_xlabel.assert_called_once_with(constants.DataFrameColumns.DATE)
        mock_ylabel.assert_called_once_with(constants.PRICE_USD_LABEL)
        mock_title.assert_called_once_with(
            f"{sample_data.SAMPLE_TICKER.upper()}{constants.CLOSING_PRICES_TITLE_SUFFIX}"
        )
        mock_grid.assert_called_once_with(True)
        mock_legend.assert_called_once()
        mock_xticks.assert_called_once_with(rotation=constants.X_AXIS_ROTATION)
        mock_tight_layout.assert_called_once()

    @patch("builtins.print")
    @patch("matplotlib.pyplot.savefig")
    @patch("matplotlib.pyplot.show")
    def test_save_plot_prints_save_message(  # noqa: PLR0913
        self,
        mock_show: Mock,
        mock_savefig: Mock,
        mock_print: Mock,
        sample_df: pd.DataFrame,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test that save_plot prints a message about where the plot was saved."""
        monkeypatch.chdir(tmp_path)

        plot.save_plot(sample_df, sample_data.SAMPLE_TICKER)

        # Check that print was called with the save message
        expected_path = (
            Path(constants.Directories.GRAPHS)
            / f"{sample_data.SAMPLE_TICKER}{constants.PLOT_SUFFIX}"
        )
        mock_print.assert_called_with(f"Plot saved to {expected_path}")

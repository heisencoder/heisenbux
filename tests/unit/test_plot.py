"""Unit tests for plot module."""

import tempfile
from collections.abc import Generator
from pathlib import Path
from unittest.mock import Mock, patch

import pandas as pd
import pytest

from heisenbux.plot import save_plot
from tests.fixtures.sample_data import SAMPLE_TICKER, create_sample_dataframe


class TestSavePlot:
    """Test cases for save_plot function."""

    @pytest.fixture
    def sample_df(self) -> pd.DataFrame:
        """Get sample DataFrame for testing."""
        return create_sample_dataframe()

    @pytest.fixture
    def temp_graphs_dir(self) -> Generator[Path, None, None]:
        """Create a temporary graphs directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @patch("matplotlib.pyplot.savefig")
    @patch("matplotlib.pyplot.show")
    def test_save_plot_saves_file(  # noqa: PLR0913
        self,
        mock_show: Mock,
        mock_savefig: Mock,
        sample_df: pd.DataFrame,
        temp_graphs_dir: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test that save_plot saves the plot file."""
        monkeypatch.chdir(temp_graphs_dir)

        save_plot(sample_df, SAMPLE_TICKER)

        # Check that savefig was called
        mock_savefig.assert_called_once()
        save_args = mock_savefig.call_args[0]
        expected_path = Path("graphs") / f"{SAMPLE_TICKER}_plot.png"
        assert save_args[0] == expected_path

        # Check that show was called
        mock_show.assert_called_once()

    @patch("matplotlib.pyplot.savefig")
    def test_save_plot_creates_graphs_directory(
        self,
        mock_savefig: Mock,
        sample_df: pd.DataFrame,
        temp_graphs_dir: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test that save_plot creates graphs directory if it doesn't exist."""
        monkeypatch.chdir(temp_graphs_dir)

        graphs_dir = Path("graphs")
        assert not graphs_dir.exists()

        with patch("matplotlib.pyplot.show"):
            save_plot(sample_df, SAMPLE_TICKER)

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
        temp_graphs_dir: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test that save_plot creates a plot with correct properties."""
        monkeypatch.chdir(temp_graphs_dir)

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
            save_plot(sample_df, SAMPLE_TICKER)

        # Check that figure was created with correct size
        mock_figure.assert_called_once_with(figsize=(12, 6))

        # Check that plot was called with correct data
        mock_plot.assert_called_once()
        plot_args = mock_plot.call_args[0]
        assert len(plot_args[0]) == len(sample_df)  # x data (dates)
        assert len(plot_args[1]) == len(sample_df)  # y data (close prices)

        # Check labels and title
        mock_xlabel.assert_called_once_with("Date")
        mock_ylabel.assert_called_once_with("Price (USD)")
        mock_title.assert_called_once_with(
            f"{SAMPLE_TICKER.upper()} Closing Prices (Last Year)"
        )
        mock_grid.assert_called_once_with(True)
        mock_legend.assert_called_once()
        mock_xticks.assert_called_once_with(rotation=45)
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
        temp_graphs_dir: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test that save_plot prints a message about where the plot was saved."""
        monkeypatch.chdir(temp_graphs_dir)

        save_plot(sample_df, SAMPLE_TICKER)

        # Check that print was called with the save message
        expected_path = Path("graphs") / f"{SAMPLE_TICKER}_plot.png"
        mock_print.assert_called_with(f"Plot saved to {expected_path}")

"""Functions to assist with plotting"""

import pandas as pd
from matplotlib import pyplot

from heisenbux.constants import (
    CLOSE_COLUMN,
    CLOSING_PRICE_LABEL,
    CLOSING_PRICES_TITLE_SUFFIX,
    DATE_COLUMN,
    FIGURE_SIZE,
    GRAPHS_DIR,
    PLOT_SUFFIX,
    PRICE_USD_LABEL,
    X_AXIS_ROTATION,
)
from heisenbux.utils import build_file_path, ensure_directory_exists


def save_plot(df: pd.DataFrame, ticker: str) -> None:
    """Create and save a price plot for the given ticker data.

    Args:
        df: DataFrame containing stock data with 'Close' column
        ticker: Stock ticker symbol for labeling
    """
    graphs_dir = ensure_directory_exists(GRAPHS_DIR)

    # Create and display the plot
    pyplot.figure(figsize=FIGURE_SIZE)
    pyplot.plot(df.index, df[CLOSE_COLUMN], label=CLOSING_PRICE_LABEL)
    pyplot.title(f"{ticker.upper()}{CLOSING_PRICES_TITLE_SUFFIX}")
    pyplot.xlabel(DATE_COLUMN)
    pyplot.ylabel(PRICE_USD_LABEL)
    pyplot.grid(True)
    pyplot.legend()

    # Rotate x-axis labels for better readability
    pyplot.xticks(rotation=X_AXIS_ROTATION)
    pyplot.tight_layout()

    # Save the plot to graphs directory
    plot_file = build_file_path(graphs_dir, ticker, PLOT_SUFFIX)
    pyplot.savefig(plot_file)
    print(f"Plot saved to {plot_file}")

    # Show the plot
    pyplot.show()

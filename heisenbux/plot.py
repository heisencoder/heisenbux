"""Functions to assist with plotting"""

import pandas as pd
from matplotlib import pyplot

from heisenbux import constants, directory_utils


def save_plot(df: pd.DataFrame, ticker: str) -> None:
    """Create and save a price plot for the given ticker data.

    Args:
        df: DataFrame containing stock data with 'Close' column
        ticker: Stock ticker symbol for labeling
    """
    graphs_dir = directory_utils.ensure_directory_exists(constants.Directories.GRAPHS)

    # Create and display the plot
    pyplot.figure(figsize=constants.FIGURE_SIZE)
    pyplot.plot(
        df.index,
        df[constants.DataFrameColumns.CLOSE],
        label=constants.CLOSING_PRICE_LABEL,
    )
    pyplot.title(f"{ticker.upper()}{constants.CLOSING_PRICES_TITLE_SUFFIX}")
    pyplot.xlabel(constants.DataFrameColumns.DATE)
    pyplot.ylabel(constants.PRICE_USD_LABEL)
    pyplot.grid(True)
    pyplot.legend()

    # Rotate x-axis labels for better readability
    pyplot.xticks(rotation=constants.X_AXIS_ROTATION)
    pyplot.tight_layout()

    # Save the plot to graphs directory
    plot_file = directory_utils.build_file_path(
        graphs_dir, ticker, constants.PLOT_SUFFIX
    )
    pyplot.savefig(plot_file)
    print(f"Plot saved to {plot_file}")

    # Show the plot
    pyplot.show()

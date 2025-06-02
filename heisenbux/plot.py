"""Functions to assist with plotting"""

from pathlib import Path

import pandas as pd
from matplotlib import pyplot


def save_plot(df: pd.DataFrame, ticker: str) -> None:
    """Create and save a price plot for the given ticker data.

    Args:
        df: DataFrame containing stock data with 'Close' column
        ticker: Stock ticker symbol for labeling
    """
    graphs_dir: Path = Path("graphs")
    graphs_dir.mkdir(parents=True, exist_ok=True)

    # Create and display the plot
    pyplot.figure(figsize=(12, 6))
    pyplot.plot(df.index, df["Close"], label="Closing Price")
    pyplot.title(f"{ticker.upper()} Closing Prices (Last Year)")
    pyplot.xlabel("Date")
    pyplot.ylabel("Price (USD)")
    pyplot.grid(True)
    pyplot.legend()

    # Rotate x-axis labels for better readability
    pyplot.xticks(rotation=45)
    pyplot.tight_layout()

    # Save the plot to graphs directory
    plot_file: Path = graphs_dir / f"{ticker.upper()}_plot.png"
    pyplot.savefig(plot_file)
    print(f"Plot saved to {plot_file}")

    # Show the plot
    pyplot.show()

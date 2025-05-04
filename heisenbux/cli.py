"""Command line interface for Heisenbux."""

import click

from heisenbux import plot
from heisenbux import finance


@click.command()
@click.argument("ticker")
@click.option(
    "--show-plot/--no-show-plot",
    default=True,
    help="Whether to display the price plot (default: True)",
)
@click.option(
    "--force-download/--no-force-download",
    default=False,
    help="Force download new data even if cached (default: False)",
)
def main(ticker: str, show_plot: bool, force_download: bool):
    """Fetch the last year of daily price data for a given stock ticker and save it to a CSV file.

    Args:
        ticker: The stock ticker symbol (e.g., AAPL, GOOGL)
    """
    df = finance.get_ticker_data(ticker, force_download)

    if show_plot:
        plot.save_plot(df, ticker)


if __name__ == "__main__":
    main()

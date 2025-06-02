"""Script to download data for popular Vanguard funds."""

import subprocess  # nosec B404

from heisenbux.constants import (
    NO_FORCE_DOWNLOAD_FLAG,
    NO_SHOW_PLOT_FLAG,
    POETRY_RUN_HEISENBUX,
    SHOW_PLOT_FLAG,
)


def _run_heisenbux_command(ticker: str, flags: list[str]) -> None:
    """Run heisenbux CLI command with given flags.

    Args:
        ticker: Stock ticker symbol
        flags: List of CLI flags to pass
    """
    subprocess.run(  # nosec B603, B607
        [*POETRY_RUN_HEISENBUX, ticker, *flags], check=True
    )


def download_funds(funds: list[str]) -> None:
    """Download data for a list of Vanguard funds."""
    for fund in funds:
        print(f"\nDownloading data for {fund}...")
        _run_heisenbux_command(fund, [NO_SHOW_PLOT_FLAG])


def generate_plots(funds: list[str]) -> None:
    """Generate plots for a list of Vanguard funds."""
    for fund in funds:
        print(f"\nGenerating plot for {fund}...")
        _run_heisenbux_command(fund, [NO_FORCE_DOWNLOAD_FLAG, SHOW_PLOT_FLAG])


if __name__ == "__main__":
    vanguard_funds: list[str] = [
        "VTI",  # Vanguard Total Stock Market ETF
        "VOO",  # Vanguard S&P 500 ETF
        "VXUS",  # Vanguard Total International Stock ETF
        "BND",  # Vanguard Total Bond Market ETF
        "VNQ",  # Vanguard Real Estate ETF
        "VGT",  # Vanguard Information Technology ETF
        "VYM",  # Vanguard High Dividend Yield ETF
        "VUG",  # Vanguard Growth ETF
        "VB",  # Vanguard Small-Cap ETF
        "VTV",  # Vanguard Value ETF
    ]

    # First ensure all data is downloaded
    download_funds(vanguard_funds)
    print("\nAll downloads completed!")

    # Then generate plots for all funds
    print("\nGenerating plots for all funds...")
    generate_plots(vanguard_funds)
    print("\nAll plots generated!")

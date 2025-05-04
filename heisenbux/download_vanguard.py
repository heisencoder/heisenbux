"""Script to download data for popular Vanguard funds."""

import subprocess
from typing import List


def download_funds(funds: List[str]) -> None:
    """Download data for a list of Vanguard funds."""
    for fund in funds:
        print(f"\nDownloading data for {fund}...")
        subprocess.run(["poetry", "run", "heisenbux", fund, "--no-show-plot"], check=True)


def generate_plots(funds: List[str]) -> None:
    """Generate plots for a list of Vanguard funds."""
    for fund in funds:
        print(f"\nGenerating plot for {fund}...")
        subprocess.run(["poetry", "run", "heisenbux", fund, "--no-force-download", "--show-plot"], check=True)


if __name__ == "__main__":
    vanguard_funds = [
        "VTI",  # Vanguard Total Stock Market ETF
        "VOO",  # Vanguard S&P 500 ETF
        "VXUS",  # Vanguard Total International Stock ETF
        "BND",  # Vanguard Total Bond Market ETF
        "VNQ",  # Vanguard Real Estate ETF
        "VGT",  # Vanguard Information Technology ETF
        "VYM",  # Vanguard High Dividend Yield ETF
        "VUG",  # Vanguard Growth ETF
        "VB",   # Vanguard Small-Cap ETF
        "VTV",  # Vanguard Value ETF
    ]

    # First ensure all data is downloaded
    download_funds(vanguard_funds)
    print("\nAll downloads completed!")

    # Then generate plots for all funds
    print("\nGenerating plots for all funds...")
    generate_plots(vanguard_funds)
    print("\nAll plots generated!")

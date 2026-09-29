"""Create the practice input data: daily prices and company facts.

This stands in for a real download (WRDS, Sequantis, NGFS...). The data is
synthetic, so nobody needs credentials to follow the tutorial.

    python make_data.py            # first version of the data
    python make_data.py --update   # a "refreshed" version: 20 more, stormier trading days
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd

COMPANIES = pd.DataFrame(
    {
        "company": ["Alpine Steel", "Blue Wind", "Coastal Cement", "Delta Retail", "Echo Airlines"],
        "sector": ["Steel", "Utilities", "Materials", "Retail", "Transport"],
        "emissions_t": [1_200_000, 40_000, 900_000, 25_000, 450_000],  # tonnes CO2 per year
        "profit_eur": [310e6, 120e6, 205e6, 150e6, 95e6],  # yearly operating profit
    }
)


def make_prices(days: int, stormy_days: int = 0, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range("2025-01-02", periods=days)
    vols = np.array([0.020, 0.012, 0.018, 0.010, 0.025])  # daily volatility per company
    shocks = rng.normal(0.0003, vols, size=(days, len(vols)))
    if stormy_days:
        shocks[-stormy_days:] *= 2.5  # a market sell-off at the end
    prices = 100 * np.exp(np.cumsum(shocks, axis=0))
    return pd.DataFrame(prices.round(4), index=dates, columns=COMPANIES["company"]).rename_axis("date")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--update", action="store_true", help="add 20 trading days")
    args = parser.parse_args()

    Path("data").mkdir(exist_ok=True)
    days = 270 if args.update else 250
    make_prices(days, stormy_days=20 if args.update else 0).to_csv("data/prices.csv", lineterminator="\n")
    COMPANIES.to_csv("data/companies.csv", index=False, lineterminator="\n")
    print(f"Wrote data/prices.csv ({days} trading days) and data/companies.csv")


if __name__ == "__main__":
    main()

"""Stage 1: turn daily prices into daily returns."""
from pathlib import Path

import numpy as np
import pandas as pd

prices = pd.read_csv("data/prices.csv", index_col="date", parse_dates=True)
returns = np.log(prices / prices.shift(1)).dropna()

Path("data").mkdir(exist_ok=True)
returns.round(6).to_csv("data/returns.csv", lineterminator="\n")
print(f"Wrote data/returns.csv ({len(returns)} days)")

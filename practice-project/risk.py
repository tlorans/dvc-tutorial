"""Stage 2: portfolio Value at Risk (VaR) from daily returns.

Settings come from the `risk` section of params.yaml, so DVC reruns this
stage when one of them changes.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

params = yaml.safe_load(open("params.yaml"))["risk"]
returns = pd.read_csv("data/returns.csv", index_col="date", parse_dates=True)

weights = pd.Series(params["weights"])
window = returns[weights.index].tail(params["window_days"])
portfolio = window @ weights

confidence = params["confidence"]
var = -np.quantile(portfolio, 1 - confidence)  # historical VaR, as a positive loss
volatility = portfolio.std() * np.sqrt(252)  # annualised

Path("data").mkdir(exist_ok=True)
Path("metrics").mkdir(exist_ok=True)
portfolio.round(6).to_frame("portfolio_return").to_csv("data/portfolio_returns.csv", lineterminator="\n")
metrics = {
    "confidence": confidence,
    "window_days": params["window_days"],
    "one_day_var_pct": round(100 * var, 3),
    "annual_volatility_pct": round(100 * volatility, 3),
}
json.dump(metrics, open("metrics/risk.json", "w", newline="\n"), indent=2)
print(f"1-day VaR at {confidence:.0%}: {metrics['one_day_var_pct']}% of portfolio value")

"""Stage 3: a simple carbon-price stress test.

Each company pays `emissions_t * carbon_price_eur` more per year. We express
that extra cost as a share of its operating profit. This is the same idea as
the cash-flow shock stage of a real climate-risk model, in a few lines.
"""
import json
from pathlib import Path

import pandas as pd
import yaml

scenario = yaml.safe_load(open("params.yaml"))["scenario"]
companies = pd.read_csv("data/companies.csv")

price = scenario["carbon_price_eur"]
companies["extra_cost_eur"] = companies["emissions_t"] * price
companies["profit_hit_pct"] = (100 * companies["extra_cost_eur"] / companies["profit_eur"]).round(1)

Path("data").mkdir(exist_ok=True)
Path("metrics").mkdir(exist_ok=True)
companies.to_csv("data/stressed.csv", index=False, lineterminator="\n")
worst = companies.loc[companies["profit_hit_pct"].idxmax()]
metrics = {
    "scenario": scenario["name"],
    "carbon_price_eur": price,
    "average_profit_hit_pct": round(companies["profit_hit_pct"].mean(), 1),
    "worst_company": worst["company"],
    "worst_profit_hit_pct": float(worst["profit_hit_pct"]),
}
json.dump(metrics, open("metrics/stress.json", "w", newline="\n"), indent=2)
print(f"{scenario['name']}: worst hit {worst['company']} ({worst['profit_hit_pct']}% of profit)")

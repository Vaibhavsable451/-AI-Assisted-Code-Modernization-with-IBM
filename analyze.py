# analyze.py
# Breakdown history associates risk most with distance since service, followed by daily usage
# and load factor; lifetime mileage and age have virtually no separation between outcomes.
# A weighted percentile score ranks cars by those three usage patterns, without changing the
# separate 80% service-wear rule.

import pandas as pd

FEATURE_WEIGHTS = {
    "km_since_service": 0.46,
    "avg_daily_km": 0.29,
    "load_factor": 0.25,
}
COMPARISON_COLUMNS = [
    "odometer_km",
    "km_since_service",
    "avg_daily_km",
    "load_factor",
    "age_years",
]


def rank_risk(history: pd.DataFrame) -> pd.DataFrame:
    """Score cars from 0 to 100 using weighted ranks of observed risk factors."""
    required = set(FEATURE_WEIGHTS) | {"car_id"}
    missing = required.difference(history.columns)
    if missing:
        raise ValueError(f"Missing required history columns: {', '.join(sorted(missing))}")

    feature_ranks = history[list(FEATURE_WEIGHTS)].rank(pct=True)
    weights = pd.Series(FEATURE_WEIGHTS)
    weighted_rank = feature_ranks.mul(weights).sum(axis=1)
    spread = weighted_rank.max() - weighted_rank.min()

    ranked = history.copy()
    if spread == 0:
        ranked["risk_score"] = 50.0
    else:
        ranked["risk_score"] = ((weighted_rank - weighted_rank.min()) / spread * 100).round(1)
    return ranked.sort_values(["risk_score", "car_id"], ascending=[False, True])


def main() -> None:
    """Compare historical outcomes and print all cars in risk order."""
    history = pd.read_csv("fleet_history.csv")
    missing = set(COMPARISON_COLUMNS + ["broke_down"]).difference(history.columns)
    if missing:
        raise ValueError(f"Missing required history columns: {', '.join(sorted(missing))}")

    print("Mean historical values by breakdown outcome (0 = no, 1 = yes):")
    print(history.groupby("broke_down")[COMPARISON_COLUMNS].mean().T.to_string())
    print("\nCars ranked by estimated breakdown risk (0-100):")
    ranked = rank_risk(history)
    print(ranked[["car_id", "risk_score"]].to_string(index=False))


if __name__ == "__main__":
    main()

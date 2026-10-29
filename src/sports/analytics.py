"""Historical threshold rates, Wilson intervals, and chronological evaluation."""

import math
from itertools import groupby


def wilson_interval(successes, count):
    if count < 1 or not 0 <= successes <= count:
        raise ValueError("Wilson interval requires 0 <= successes <= count and count > 0")
    z = 1.959963984540054
    rate = successes / count
    denominator = 1 + z * z / count
    center = (rate + z * z / (2 * count)) / denominator
    radius = z * math.sqrt(rate * (1 - rate) / count + z * z / (4 * count * count)) / denominator
    return [max(0.0, center - radius), min(1.0, center + radius)]


def chronological_evaluation(series, threshold, minimum_history=5):
    """Estimate each date using only earlier dates, including no same-day outcomes."""
    series = sorted(series, key=lambda row: (row["date"], row["game_id"]))
    history, predictions = [], []
    for played, group in groupby(series, key=lambda row: row["date"]):
        current = list(group)
        if len(history) >= minimum_history:
            probability = (sum(history) + 1) / (len(history) + 2)
            predictions.extend({
                "date": played, "game_id": row["game_id"],
                "history_count": len(history), "probability": probability,
                "outcome": int(row["value"] > threshold),
            } for row in current)
        history.extend(int(row["value"] > threshold) for row in current)
    count = len(predictions)
    return {
        "method": "Expanding history with Laplace smoothing; earlier dates only",
        "minimum_history": minimum_history, "evaluated_games": count,
        "brier_score": sum((row["probability"] - row["outcome"]) ** 2
                           for row in predictions) / count if count else None,
        "constant_half_brier_score": 0.25 if count else None,
        "predictions": predictions,
    }


def analyze(store, team, player=None, opponent=None, threshold=20.5):
    if not math.isfinite(threshold) or not 0 <= threshold <= 1000:
        raise ValueError("Threshold must be a finite number from 0 to 1000")
    rows = store.select(team, player, opponent)
    games = {row["game_id"]: row for row in rows}
    selected = rows if player else list(games.values())
    series = [{"game_id": row["game_id"], "date": row["date"],
               "opponent": row["opponent"],
               "value": row["points"] if player else row["team_score"]}
              for row in selected]
    series.sort(key=lambda row: (row["date"], row["game_id"]))
    count = len(series)
    successes = sum(row["value"] > threshold for row in series)
    mean = sum(row["value"] for row in series) / count if count else None
    return {
        "dataset": store.metadata(),
        "selection": {"team": team, "player": player, "opponent": opponent,
                      "threshold": threshold, "metric": "Player points" if player else "Team points"},
        "summary": {
            "games": count, "mean_points": mean,
            "wins": sum(row["team_score"] > row["opponent_score"] for row in games.values()),
            "losses": sum(row["team_score"] < row["opponent_score"] for row in games.values()),
            "draws": sum(row["team_score"] == row["opponent_score"] for row in games.values()),
            "exceeded_threshold": successes,
            "historical_rate": successes / count if count else None,
            "wilson_95_interval": wilson_interval(successes, count) if count else None,
        },
        "series": series, "evaluation": chronological_evaluation(series, threshold),
        "interpretation": "Historical frequency is not a validated probability for the next game. "
                          "The Wilson interval assumes comparable independent observations; "
                          "schedule, roster, and selection changes can violate that assumption.",
    }

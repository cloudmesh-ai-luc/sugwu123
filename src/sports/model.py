"""A small online logistic classifier with strictly historical input features."""

import math
from itertools import groupby

from .analytics import analyze
from .config import CONFIG


def evaluate_model(series, threshold, minimum_history=None, learning_rate=None):
    """Predict before learning each date; score all baselines on the same games."""
    if minimum_history is None:
        minimum_history = int(CONFIG["minimum_history"])
    if learning_rate is None:
        learning_rate = float(CONFIG["learning_rate"])
    scale = float(CONFIG["feature_scale"])
    min_train = int(CONFIG["training_starts_after"])

    history, weights, predictions = [], [0.0, 0.0, 0.0], []
    positives = 0
    for played, group in groupby(sorted(series, key=lambda r: (r["date"], r["game_id"])),
                                 key=lambda r: r["date"]):
        current = list(group)
        if len(history) >= min_train:
            features = [1.0, (sum(history[-min_train:]) / min_train - threshold) / scale,
                        (history[-1] - threshold) / scale]
            logit = sum(w * x for w, x in zip(weights, features))
            probability = 1 / (1 + math.exp(-max(-35.0, min(35.0, logit))))
            historical = (positives + 1) / (len(history) + 2)
            outcomes = [int(row["value"] > threshold) for row in current]
            if len(history) >= minimum_history:
                predictions.extend({"date": played, "game_id": row["game_id"],
                                    "history_count": len(history), "features": features[:],
                                    "probability": probability, "historical_probability": historical,
                                    "outcome": outcome}
                                   for row, outcome in zip(current, outcomes))
            error = sum(probability - outcome for outcome in outcomes) / len(outcomes)
            weights = [w - learning_rate * error * x for w, x in zip(weights, features)]
        history.extend(row["value"] for row in current)
        positives += sum(row["value"] > threshold for row in current)
    count = len(predictions)

    def score(field):
        return sum((row[field] - row["outcome"]) ** 2 for row in predictions) / count if count else None

    return {"method": "Online logistic regression; earlier dates only",
            "features": ["intercept", "prior five-game mean minus threshold / 20",
                         "previous-game points minus threshold / 20"],
            "learning_rate": learning_rate, "training_starts_after": min_train,
            "minimum_evaluation_history": minimum_history, "evaluated_games": count,
            "logistic_brier_score": score("probability"),
            "historical_brier_score": score("historical_probability"),
            "constant_half_brier_score": 0.25 if count else None,
            "predictions": predictions}


def analyze_model(store, team, player=None, opponent=None, threshold=None):
    if threshold is None:
        threshold = float(CONFIG["default_model_threshold"])
    result = analyze(store, team, player, opponent, threshold)
    return {"dataset": result["dataset"], "selection": result["selection"],
            "model": evaluate_model(result["series"], threshold),
            "interpretation": "One selected historical sample does not establish future accuracy. "
                              "Filters and thresholds must be fixed before examining evaluation scores."}

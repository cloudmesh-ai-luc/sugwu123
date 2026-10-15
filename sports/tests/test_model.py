import unittest
from datetime import date, timedelta

from sports.model import evaluate_model


class ModelTests(unittest.TestCase):
    def series(self):
        return [{"game_id": str(i), "date": str(date(2020, 1, 1) + timedelta(days=i)),
                 "value": 90 + (i * 7) % 25} for i in range(30)]

    def test_future_scores_do_not_change_earlier_forecasts(self):
        rows = self.series()
        before = evaluate_model(rows, 100.5)
        changed = [dict(row, value=1000) if i >= 22 else row for i, row in enumerate(rows)]
        after = evaluate_model(changed, 100.5)
        self.assertEqual(before["predictions"][:12], after["predictions"][:12])

    def test_same_day_results_do_not_change_same_day_predictions(self):
        rows = self.series()
        rows[11]["date"] = rows[10]["date"]
        original = evaluate_model(rows, 100.5)["predictions"]
        rows[10]["value"] = 1000
        changed = evaluate_model(rows, 100.5)["predictions"]
        self.assertEqual(original[1]["probability"], changed[1]["probability"])
        self.assertEqual(original[1]["features"], changed[1]["features"])

    def test_features_use_previous_five_games_and_baselines_share_cohort(self):
        rows = self.series()
        result = evaluate_model(rows, 100.5)
        first = result["predictions"][0]
        self.assertEqual(first["history_count"], 10)
        self.assertAlmostEqual(first["features"][1], (sum(r["value"] for r in rows[5:10]) / 5 - 100.5) / 20)
        self.assertEqual(result["evaluated_games"], 20)
        score = sum((r["historical_probability"] - r["outcome"]) ** 2 for r in result["predictions"]) / 20
        self.assertAlmostEqual(result["historical_brier_score"], score)
        self.assertEqual(result["constant_half_brier_score"], 0.25)

    def test_short_series_has_no_claimed_evaluation(self):
        result = evaluate_model(self.series()[:9], 100.5)
        self.assertEqual(result["evaluated_games"], 0)
        self.assertIsNone(result["logistic_brier_score"])

    def test_extreme_valid_scores_keep_finite_probabilities(self):
        result = evaluate_model([dict(r, value=1000) for r in self.series()], 0)
        self.assertTrue(all(0 <= r["probability"] <= 1 for r in result["predictions"]))

import contextlib
import csv
import io
import json
import math
import subprocess
import sys
import tarfile
import tempfile
import threading
import unittest
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from unittest.mock import patch

from sports.analytics import analyze, chronological_evaluation, wilson_interval
from sports.demo import demo_rows
from sports.server import make_server
from sports.store import FIELDS, Store, read_csv
from sports.vm import archive_source, main as vm_main, validate_name


def fixture_rows():
    return [{"game_id": f"game-{index}", "date": f"2025-01-0{index + 1}",
             "team": "A", "opponent": "B", "player": "Pat", "points": value,
             "team_score": 100, "opponent_score": 90 if index % 2 == 0 else 110}
            for index, value in enumerate([10, 20, 30, 40])]


def seed(store, rows=None):
    return store.replace(rows if rows is not None else fixture_rows(), kind="synthetic",
                         source="Test fixture", rights="Generated test observations")


class AnalyticsTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.store = Store(Path(self.temporary.name) / "sports.sqlite3")
        seed(self.store)

    def test_known_rate_and_strict_threshold(self):
        summary = analyze(self.store, "A", "Pat", threshold=20)["summary"]
        self.assertEqual(summary["games"], 4)
        self.assertEqual(summary["exceeded_threshold"], 2)
        self.assertEqual(summary["historical_rate"], 0.5)
        self.assertEqual(summary["mean_points"], 25)
        self.assertEqual((summary["wins"], summary["losses"]), (2, 2))

    def test_wilson_reference_values(self):
        lower, upper = wilson_interval(5, 10)
        self.assertAlmostEqual(lower, 0.2365930905, places=9)
        self.assertAlmostEqual(upper, 0.7634069095, places=9)

    def test_wilson_extreme_rates_have_uncertainty(self):
        lower, upper = wilson_interval(0, 10)
        self.assertAlmostEqual(lower, 0)
        self.assertGreater(upper, 0.27)
        lower, upper = wilson_interval(10, 10)
        self.assertLess(lower, 0.73)
        self.assertAlmostEqual(upper, 1)
        with self.assertRaises(ValueError):
            wilson_interval(0, 0)

    def test_team_games_not_counted_once_per_player(self):
        rows = fixture_rows()
        rows += [dict(row, player="Robin", points=5) for row in fixture_rows()]
        self.store.replace(rows, kind="synthetic", source="Fixture", rights="Generated", replace=True)
        summary = analyze(self.store, "A", threshold=99.5)["summary"]
        self.assertEqual(summary["games"], 4)
        self.assertEqual(summary["exceeded_threshold"], 4)
        self.assertEqual(summary["mean_points"], 100)
        self.assertEqual(summary["wins"], 2)

    def test_chronological_evaluation_excludes_same_day_and_future(self):
        series = [{"date": "2025-01-01", "game_id": "1", "value": 10},
                  {"date": "2025-01-02", "game_id": "2", "value": 30},
                  {"date": "2025-01-02", "game_id": "3", "value": 30},
                  {"date": "2025-01-03", "game_id": "4", "value": 0}]
        evaluation = chronological_evaluation(list(reversed(series)), 20, minimum_history=1)
        predictions = evaluation["predictions"]
        self.assertEqual(evaluation["evaluated_games"], 3)
        self.assertEqual([row["history_count"] for row in predictions], [1, 1, 3])
        self.assertAlmostEqual(predictions[0]["probability"], 1 / 3)
        self.assertAlmostEqual(predictions[1]["probability"], 1 / 3)
        self.assertAlmostEqual(predictions[2]["probability"], 3 / 5)
        self.assertAlmostEqual(evaluation["brier_score"], (8 / 9 + 0.36) / 3)
        series[-1]["value"] = 999
        changed = chronological_evaluation(series, 20, minimum_history=1)
        self.assertEqual(changed["predictions"][:2], predictions[:2])

    def test_insufficient_history_has_no_evaluation_score(self):
        evaluation = analyze(self.store, "A", "Pat")["evaluation"]
        self.assertEqual(evaluation["evaluated_games"], 0)
        self.assertIsNone(evaluation["brier_score"])

    def test_empty_filter_combination_has_no_rate(self):
        rows = fixture_rows() + [dict(fixture_rows()[0], game_id="extra", player="Robin", opponent="C")]
        self.store.replace(rows, kind="synthetic", source="Fixture", rights="Generated", replace=True)
        summary = analyze(self.store, "A", "Pat", "C")["summary"]
        self.assertEqual(summary["games"], 0)
        self.assertIsNone(summary["historical_rate"])
        self.assertIsNone(summary["wilson_95_interval"])

    def test_nonfinite_and_out_of_range_thresholds_are_rejected(self):
        for threshold in [math.nan, math.inf, -math.inf, -1, 1001]:
            with self.subTest(threshold=threshold), self.assertRaises(ValueError):
                analyze(self.store, "A", threshold=threshold)


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.store = Store(Path(self.temporary.name) / "sports.sqlite3")

    def test_demo_reproducibility_and_expected_shape(self):
        first, second = demo_rows(), demo_rows()
        self.assertEqual(first, second)
        self.assertEqual(len(first), 144)
        seed(self.store, first)
        options = self.store.options()
        self.assertEqual(len(options["teams"]), 4)
        result = analyze(self.store, "Lake City Lynx", "Morgan Lee", threshold=20.5)
        self.assertEqual(result["summary"]["games"], 18)
        self.assertEqual(result["evaluation"]["evaluated_games"], 13)

    def test_csv_round_trip_and_provenance_persist(self):
        path = Path(self.temporary.name) / "fixture.csv"
        with path.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(fixture_rows())
        rows = read_csv(path)
        self.store.replace(rows, kind="imported", source="https://example.invalid/fixture",
                           rights="Synthetic test fixture")
        reopened = Store(self.store.path)
        self.assertEqual(reopened.metadata()["kind"], "imported")
        self.assertEqual(reopened.select("A"), fixture_rows())

    def test_invalid_replacement_preserves_prior_data(self):
        metadata = seed(self.store)
        rows = fixture_rows()
        rows[-1]["points"] = -1
        with self.assertRaises(ValueError):
            self.store.replace(rows, kind="synthetic", source="New", rights="Generated", replace=True)
        self.assertEqual(self.store.select("A"), fixture_rows())
        self.assertEqual(self.store.metadata(), metadata)

    def test_replacement_requires_explicit_flag(self):
        seed(self.store)
        with self.assertRaises(ValueError):
            seed(self.store, demo_rows())
        self.assertEqual(len(self.store.select("A")), 4)

    def test_duplicate_player_and_inconsistent_score_are_rejected(self):
        for rows in [fixture_rows() + [fixture_rows()[0]],
                     fixture_rows() + [dict(fixture_rows()[0], player="Robin", team_score=101)]]:
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                seed(self.store, rows)
        self.assertEqual(self.store.metadata()["kind"], "empty")

    def test_reverse_team_score_consistency(self):
        original = fixture_rows()[0]
        reversed_row = dict(original, team="B", opponent="A", player="Opponent",
                            team_score=90, opponent_score=100)
        seed(self.store, [original, reversed_row])
        self.assertEqual(analyze(self.store, "B")["summary"]["losses"], 1)
        reversed_row["opponent_score"] = 101
        with self.assertRaises(ValueError):
            self.store.replace([original, reversed_row], kind="synthetic", source="Fixture",
                               rights="Generated", replace=True)

    def test_import_requires_source_url_and_rights(self):
        for source, rights in [("local file", "Permitted"), ("https:", "Permitted"),
                              ("https://example.invalid", "")]:
            with self.subTest(source=source, rights=rights), self.assertRaises(ValueError):
                self.store.replace(fixture_rows(), kind="imported", source=source, rights=rights)

    def test_sql_values_are_bound_as_literals(self):
        unusual_team = "A' OR 1=1 --"
        rows = fixture_rows() + [dict(fixture_rows()[0], game_id="extra", team=unusual_team)]
        seed(self.store, rows)
        self.assertEqual(len(self.store.select(unusual_team)), 1)


class APITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory()
        cls.store = Store(Path(cls.temporary.name) / "sports.sqlite3")
        seed(cls.store, demo_rows())
        cls.server = make_server(cls.store, port=0)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()
        cls.temporary.cleanup()

    def get_json(self, path):
        with urllib.request.urlopen(self.base + path, timeout=5) as response:
            return json.load(response)

    def test_health_and_options(self):
        self.assertEqual(self.get_json("/api/health")["status"], "ok")
        options = self.get_json("/api/options")
        self.assertEqual(options["dataset"]["kind"], "synthetic")
        self.assertEqual(len(options["teams"]), 4)

    def test_api_and_cli_return_same_analysis(self):
        query = urllib.parse.urlencode({"team": "Lake City Lynx", "player": "Morgan Lee", "threshold": 20.5})
        result = self.get_json("/api/analyze?" + query)
        command = subprocess.run([sys.executable, "-m", "sports", "--db", str(self.store.path),
                                  "analyze", "--team", "Lake City Lynx", "--player", "Morgan Lee",
                                  "--threshold", "20.5"], check=True, capture_output=True, text=True)
        self.assertEqual(json.loads(command.stdout), result)

    def test_invalid_parameters_return_400_json(self):
        for query in ["team=missing", "team=Lake+City+Lynx&threshold=nan", "team=A&team=B",
                      "team=Lake+City+Lynx&extra=x", "team=Lake+City+Lynx&player=unknown"]:
            with self.subTest(query=query), self.assertRaises(urllib.error.HTTPError) as error:
                self.get_json("/api/analyze?" + query)
            self.assertEqual(error.exception.code, 400)
            self.assertIn("error", json.load(error.exception))

    def test_static_assets_and_traversal(self):
        for path in ["/", "/app.js", "/style.css"]:
            with urllib.request.urlopen(self.base + path, timeout=5) as response:
                self.assertEqual(response.status, 200)
                self.assertGreater(len(response.read()), 100)
        with self.assertRaises(urllib.error.HTTPError) as error:
            self.get_json("/../store.py")
        self.assertEqual(error.exception.code, 404)


class DeploymentSafetyTests(unittest.TestCase):
    def test_vm_name_cannot_select_coursework_or_all_instances(self):
        for name in ["week2-vm", "week4-local", "--all", "sports-", "sports-x;rm", "sports-X"]:
            with self.subTest(name=name), self.assertRaises(ValueError):
                validate_name(name)
        self.assertEqual(validate_name("sports-midterm"), "sports-midterm")

    def test_vm_deletion_requires_exact_name_and_targets_one_vm(self):
        with patch("sports.vm.shutil.which", return_value="/usr/bin/multipass"), patch("sports.vm.run") as run:
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                vm_main(["delete", "--name", "sports-midterm", "--confirm-name", "week4-local"])
            run.assert_not_called()
            vm_main(["delete", "--name", "sports-midterm", "--confirm-name", "sports-midterm"])
            run.assert_called_once_with("delete", "--purge", "sports-midterm")

    def test_deployment_archive_excludes_data_and_symbolic_links(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "source"
            (root / "data").mkdir(parents=True)
            (root / "__init__.py").write_text("# source\n")
            (root / "data" / "private.py").write_text("# do not transfer\n")
            (root / "private.csv").write_text("private data\n")
            (root / "external.py").symlink_to(root / "data" / "private.py")
            target = Path(temporary) / "source.tar.gz"
            archive_source(target, root)
            with tarfile.open(target) as archive:
                self.assertEqual(archive.getnames(), ["sports/__init__.py"])


if __name__ == "__main__":
    unittest.main()

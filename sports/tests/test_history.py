import csv
import tempfile
import unittest
from pathlib import Path

from sports.history import season_rows
from sports.store import Store


class HistoryTests(unittest.TestCase):
    def test_import_keeps_both_team_views_and_labels_aggregates(self):
        fields = ["game_id", "lg_id", "year_id", "is_playoffs", "date_game", "team_id", "opp_id", "pts", "opp_pts"]
        rows = [["g1", "NBA", "2015", "0", "10/28/2014", "CHI", "NYK", "104", "80"],
                ["g1", "NBA", "2015", "0", "10/28/2014", "NYK", "CHI", "80", "104"],
                ["p1", "NBA", "2015", "1", "4/30/2015", "CHI", "NYK", "100", "90"],
                ["old", "NBA", "2014", "0", "1/1/2014", "CHI", "NYK", "100", "90"]]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "source.csv"
            with path.open("w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(fields)
                writer.writerows(rows)
            selected = list(season_rows(path, 2015))
            self.assertEqual(len(selected), 2)
            self.assertEqual(selected[0]["date"], "2014-10-28")
            self.assertIn("aggregate", selected[0]["player"])
            self.assertNotEqual(selected[0]["player"], selected[1]["player"])
            store = Store(Path(tmp) / "history.sqlite3")
            store.replace(selected, kind="imported", source="https://example.org/source", rights="fixture")
            self.assertEqual(len(store.select("CHI")), 1)

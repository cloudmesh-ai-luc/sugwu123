"""Validated CSV ingestion and persistent SQLite storage."""

import csv
import json
import sqlite3
from contextlib import contextmanager
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit


FIELDS = ("game_id", "date", "team", "opponent", "player", "points",
          "team_score", "opponent_score")
DEFAULT_DB = Path(__file__).resolve().parent / "data" / "sports.sqlite3"


def validate_rows(rows):
    validated, seen, games, totals = [], set(), {}, {}
    for number, raw in enumerate(rows, 2):
        if set(raw) != set(FIELDS):
            raise ValueError(f"Row {number}: expected exactly {', '.join(FIELDS)}")
        row = {}
        for field in FIELDS[:5]:
            value = str(raw[field]).strip() if raw[field] is not None else ""
            if not value or len(value) > 100 or any(ord(c) < 32 for c in value):
                raise ValueError(f"Row {number}: invalid {field}")
            row[field] = value
        try:
            if date.fromisoformat(row["date"]).isoformat() != row["date"]:
                raise ValueError
        except ValueError:
            raise ValueError(f"Row {number}: date must be YYYY-MM-DD") from None
        for field in FIELDS[5:]:
            value = str(raw[field])
            if not value.isascii() or not value.isdigit() or int(value) > 1000:
                raise ValueError(f"Row {number}: {field} must be an integer from 0 to 1000")
            row[field] = int(value)
        if row["team"] == row["opponent"] or row["points"] > row["team_score"]:
            raise ValueError(f"Row {number}: inconsistent team or player score")
        observation_key = (row["game_id"], row["player"])
        if observation_key in seen:
            raise ValueError(f"Row {number}: duplicate player in a game")
        seen.add(observation_key)
        game_key = (row["game_id"], row["team"])
        details = (row["date"], row["opponent"], row["team_score"], row["opponent_score"])
        if game_key in games and games[game_key] != details:
            raise ValueError(f"Row {number}: inconsistent game details")
        games[game_key] = details
        totals[game_key] = totals.get(game_key, 0) + row["points"]
        if totals[game_key] > row["team_score"]:
            raise ValueError(f"Row {number}: recorded players exceed team score")
        validated.append(row)
    if not validated:
        raise ValueError("The dataset contains no observations")
    by_game = {}
    for (game_id, team), details in games.items():
        by_game.setdefault(game_id, {})[team] = details
    for sides in by_game.values():
        if len(sides) > 2:
            raise ValueError("A game cannot contain more than two teams")
        if len(sides) == 2:
            (left, a), (right, b) = sides.items()
            if a != (b[0], right, b[3], b[2]) or b[1] != left:
                raise ValueError("Opposing team rows have inconsistent scores or dates")
    return validated


def read_csv(path):
    with Path(path).open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames is None or len(reader.fieldnames) != len(FIELDS):
            raise ValueError("CSV must have one header for each required column")
        return validate_rows(reader)


class Store:
    def __init__(self, path=DEFAULT_DB):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connection() as connection:
            connection.executescript("""
                CREATE TABLE IF NOT EXISTS observations (
                    game_id TEXT NOT NULL, date TEXT NOT NULL,
                    team TEXT NOT NULL, opponent TEXT NOT NULL, player TEXT NOT NULL,
                    points INTEGER NOT NULL, team_score INTEGER NOT NULL,
                    opponent_score INTEGER NOT NULL,
                    PRIMARY KEY (game_id, player)
                );
                CREATE INDEX IF NOT EXISTS team_date ON observations(team, date);
                CREATE TABLE IF NOT EXISTS metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL);
            """)

    @contextmanager
    def connection(self):
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def metadata(self):
        with self.connection() as connection:
            row = connection.execute("SELECT value FROM metadata WHERE key = 'dataset'").fetchone()
        return json.loads(row[0]) if row else {"kind": "empty", "rows": 0}

    def replace(self, rows, *, kind, source, rights, replace=False):
        # Validate the entire replacement before changing existing records.
        rows = validate_rows(rows)
        if kind not in {"synthetic", "imported"}:
            raise ValueError("Dataset kind must be synthetic or imported")
        url = urlsplit(source)
        if kind == "imported" and (url.scheme not in {"http", "https"} or not url.netloc):
            raise ValueError("Imported data requires an HTTP(S) source URL")
        if not source.strip() or not rights.strip() or len(source) > 1000 or len(rights) > 1000:
            raise ValueError("Provide a source and a data-rights statement, each at most 1000 characters")
        metadata = {"kind": kind, "source": source, "rights": rights, "rows": len(rows)}
        with self.connection() as connection:
            if connection.execute("SELECT COUNT(*) FROM observations").fetchone()[0] and not replace:
                raise ValueError("Data already exists; use --replace to deliberately replace it")
            connection.execute("DELETE FROM observations")
            connection.executemany(
                "INSERT INTO observations VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                [tuple(row[field] for field in FIELDS) for row in rows],
            )
            connection.execute("INSERT OR REPLACE INTO metadata VALUES ('dataset', ?)",
                               (json.dumps(metadata),))
        return metadata

    def options(self):
        with self.connection() as connection:
            records = connection.execute(
                "SELECT DISTINCT team, player, opponent FROM observations ORDER BY team, player, opponent"
            ).fetchall()
        teams = sorted({row["team"] for row in records})
        return {
            "dataset": self.metadata(), "teams": teams,
            "players_by_team": {team: sorted({r["player"] for r in records if r["team"] == team})
                                for team in teams},
            "opponents_by_team": {team: sorted({r["opponent"] for r in records if r["team"] == team})
                                  for team in teams},
        }

    def select(self, team, player=None, opponent=None):
        options = self.options()
        if team not in options["teams"]:
            raise ValueError("Select a team present in the dataset")
        if player and player not in options["players_by_team"][team]:
            raise ValueError("Select a player on that team")
        if opponent and opponent not in options["opponents_by_team"][team]:
            raise ValueError("Select an opponent present for that team")
        query, parameters = "SELECT * FROM observations WHERE team = ?", [team]
        for field, value in (("player", player), ("opponent", opponent)):
            if value:
                query += f" AND {field} = ?"  # Field names are fixed above, never user input.
                parameters.append(value)
        with self.connection() as connection:
            return [dict(row) for row in connection.execute(
                query + " ORDER BY date, game_id, player", parameters
            )]

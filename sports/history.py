"""Import a pinned, attributed FiveThirtyEight NBA season as team totals."""

import argparse
import csv
import hashlib
import json
import urllib.request
from datetime import datetime
from pathlib import Path

from .store import Store


REVISION = "6d880e939ad3d11d94c137c911681b3cf718fd74"
SOURCE = f"https://raw.githubusercontent.com/fivethirtyeight/data/{REVISION}/nba-elo/nbaallelo.csv"
SHA256 = "d46ed3540ee8d9eca31b3e94cc8c777e0be5156173d814ebf65b8195e8d616bc"
RIGHTS = ("FiveThirtyEight, Historical NBA Elo, CC BY 4.0; original game information: "
          "Basketball-Reference. Converted to team totals only; aggregate entries are not players.")


def download(destination):
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and hashlib.sha256(destination.read_bytes()).hexdigest() == SHA256:
        return destination
    temporary = destination.with_suffix(".part")
    try:
        total = 0
        with urllib.request.urlopen(SOURCE, timeout=30) as response, temporary.open("wb") as output:
            while chunk := response.read(1024 * 1024):
                total += len(chunk)
                if total > 32 * 1024 * 1024:
                    raise ValueError("Source exceeds the expected download size")
                output.write(chunk)
        if hashlib.sha256(temporary.read_bytes()).hexdigest() != SHA256:
            raise ValueError("Source checksum differs from the pinned dataset")
        temporary.replace(destination)
    finally:
        temporary.unlink(missing_ok=True)
    return destination


def season_rows(path, season):
    with Path(path).open(newline="", encoding="utf-8-sig") as stream:
        for row in csv.DictReader(stream):
            if row["lg_id"] != "NBA" or row["year_id"] != str(season) or row["is_playoffs"] != "0":
                continue
            team = row["team_id"]
            yield {"game_id": row["game_id"],
                   "date": datetime.strptime(row["date_game"], "%m/%d/%Y").date().isoformat(),
                   "team": team, "opponent": row["opp_id"],
                   "player": f"{team} team total (aggregate)", "points": row["pts"],
                   "team_score": row["pts"], "opponent_score": row["opp_pts"]}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--season", type=int, default=2015, help="Season ending year; regular season only")
    parser.add_argument("--db", default="sports/data/history.sqlite3")
    parser.add_argument("--source-file", default="sports/data/nbaallelo.csv")
    parser.add_argument("--replace", action="store_true")
    args = parser.parse_args(argv)
    if not 1947 <= args.season <= 2015:
        parser.error("The pinned source covers season ending years 1947 through 2015")
    try:
        source = download(args.source_file)
        result = Store(args.db).replace(season_rows(source, args.season), kind="imported",
                                        source=SOURCE, rights=RIGHTS, replace=args.replace)
        result.update(season=args.season, source_sha256=SHA256, scope="NBA regular-season team totals")
        print(json.dumps(result, indent=2))
        return 0
    except (ValueError, OSError, KeyError) as error:
        parser.exit(2, f"Error: {error}\n")


if __name__ == "__main__":
    raise SystemExit(main())

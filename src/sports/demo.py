"""Generate fictional basketball observations; no downloaded data is included."""

from datetime import date, timedelta
from random import Random


def demo_rows():
    rng = Random(388)
    teams = [
        ("Lake City Lynx", ["Morgan Lee", "Jordan Brooks"]),
        ("River Town Rockets", ["Casey Park", "Taylor Reed"]),
        ("Hillview Hawks", ["Avery Chen", "Drew Walker"]),
        ("Northside Knights", ["Riley Davis", "Sam Patel"]),
    ]
    schedules = [(0, 1, 2, 3), (0, 2, 1, 3), (0, 3, 1, 2)]
    rows = []
    for round_number in range(18):
        schedule = schedules[round_number % len(schedules)]
        played = (date(2025, 10, 1) + timedelta(days=3 * round_number)).isoformat()
        for offset in (0, 2):
            left, right = schedule[offset:offset + 2]
            left_score, right_score = rng.randint(85, 120), rng.randint(85, 120)
            if left_score == right_score:
                right_score += 1
            game_id = f"demo-{round_number + 1:02d}-{offset // 2 + 1}"
            for own, other, score, opposing in (
                (left, right, left_score, right_score),
                (right, left, right_score, left_score),
            ):
                for index, player in enumerate(teams[own][1]):
                    rows.append({
                        "game_id": game_id, "date": played,
                        "team": teams[own][0], "opponent": teams[other][0],
                        "player": player, "points": rng.randint(12, 32) - 3 * index,
                        "team_score": score, "opponent_score": opposing,
                    })
    return rows

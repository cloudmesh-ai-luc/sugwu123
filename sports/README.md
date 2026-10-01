# Sports Prototype

This implements the first application milestone of the
[Sports Statistics and Probability Analysis Platform](../project.md).
It uses Python's standard library, SQLite, a JSON API, and a web dashboard.
Python 3.12 or newer is required. No pip installation is needed.

## Run Locally

From the course repository root:

```bash
make -C sports test
make -C sports demo
make -C sports serve
```

Open <http://127.0.0.1:8000>. Stop the server with Control-C.
The demo generator creates 144 fictional player observations across 36 games,
four teams, and eight players. They are not real sports statistics.
Generated records are stored in `sports/data/sports.sqlite3`, excluded from Git.
The demo command refuses to replace existing observations unless `--replace`
is explicitly supplied. On later runs, skip `demo` if the dataset already exists.

## Command-Line and API Access

The dashboard calls the same analysis exposed through the CLI. Its purpose is
to make the game trend and uncertainty easier to inspect; core operations
require no GUI. Import and dataset creation are CLI operations.

```bash
python3 -m sports options
python3 -m sports analyze --team "Lake City Lynx" --player "Morgan Lee" --threshold 20.5
python3 -m sports analyze --team "Lake City Lynx" --opponent "River Town Rockets" --threshold 100.5
curl --fail http://127.0.0.1:8000/api/health
curl --fail --get http://127.0.0.1:8000/api/analyze \
  --data-urlencode "team=Lake City Lynx" \
  --data-urlencode "player=Morgan Lee" \
  --data-urlencode "threshold=20.5"
```

`GET /api/options` supplies the available teams, players, opponents, and source
metadata. `GET /api/analyze` accepts `team`, optional `player` and `opponent`,
and `threshold`. Unknown filters or nonfinite thresholds return HTTP 400.
Without a player filter, the metric is team points and each game counts once.
With a player filter, only games where that player has a recorded observation
are included. Opponent filters narrow the sample further.

## Import Historical Data

Select a public-domain dataset or obtain explicit usage rights first.
Prepare a local CSV with exactly these columns:

```text
game_id,date,team,opponent,player,points,team_score,opponent_score
```

Use a consistent game ID for both sides, dates as `YYYY-MM-DD`, nonnegative
integer scores, and a stable player identifier/name. Duplicate players within
a game and conflicting scorelines are rejected. The CSV may contain selected
players rather than a full roster, but their combined points cannot exceed
their team's score. DNP/missing records are not imputed as zero.

Run this with the actual source URL and license/permission statement:

```bash
python3 -m sports import /absolute/path/to/history.csv \
  --source "https://actual-dataset-source.example/path" \
  --rights "Actual license or explicit permission" --replace
```

The URL above is a placeholder, not a supplied dataset. A rights statement is
recorded provenance, not an automatic license check. The importer validates the
full dataset before replacing prior observations. Raw CSVs and generated databases
must stay outside Git. No sports API downloader has been implemented yet.

## Probability and Evaluation

For a selected sample, the event is **points strictly greater than the threshold**.
The historical rate is the number of events divided by the number of selected
games. A 95% Wilson interval describes uncertainty in that rate.[^wilson]
The independence and comparable-game assumptions may fail in real sports data.

The evaluation forecasts each date using only earlier dates. After five prior
games, the baseline probability is `(prior_events + 1) / (prior_games + 2)`.
Same-day outcomes are excluded from each other's history. The Brier score is
the mean squared error between the estimated probability and the binary outcome;
the constant 50% comparison has a score of 0.25. Thresholds and filters are user
choices, not tuned on the evaluated outcomes. Repeated selection after viewing
scores can still introduce selection bias.

Fictional-data results establish software behavior, not real forecasting skill.
Real-data evaluation and uncertainty discussion remain project tasks.

## Deploy to a Dedicated Local VM

Prerequisites on the Mac: Python 3.12+, a working Multipass installation, enough
resources for a 2-CPU/2-GB/10-GB VM, and internet access for the Ubuntu image and
any missing Python packages. From the repository root:

```bash
make -C sports vm-deploy
```

The script launches or resumes `sports-midterm` on Ubuntu 24.04, transfers only
source files, runs the tests in the guest, seeds fictional data on a fresh
deployment, configures a systemd service, checks its local health endpoint,
and prints the dashboard URL. The service listens on port 8000 inside the local
VM. It is a course demonstration server, intended for the local VM network.
Existing database content is preserved during redeployment.

```bash
make -C sports vm-status
make -C sports vm-stop
make -C sports vm-start
```

Set `NAME=sports-another-demo` to use another dedicated project VM. The script
requires a `sports-` name. It does not operate on the Week 2 or Week 4 VM names.
If the project VM is no longer needed, this explicit command deletes its disk:

```bash
python3 -m sports.vm delete --name sports-midterm --confirm-name sports-midterm
```

The helper uses `multipass delete --purge NAME`, scoped to the named instance.[^multipass]
The automated deployment was **verified on the Mac on October 1, 2026**:
`sports-midterm` was running on Ubuntu 24.04, all 23 guest tests passed, and the
service returned `status: ok` with 144 generated observations. See the
[deployment evidence](../project/vm-deployment.md). Dashboard access from the Mac
and database persistence after stop/start still require verification.
The project's native Multipass automation does not resolve the separate
Week 5 cmx failures.

## Verification and Status

The 23 automated tests cover known statistical values, counting one team game
once, chronological leakage, CSV/provenance persistence, rejected imports,
CLI/API agreement, API validation, archive exclusions, and deletion safeguards.
See [verification output](../project/verification.txt).

Remaining milestones: permitted historical data, real-data evaluation,
dashboard and persistence verification, instructor approval confirmation,
and a midterm demo.
AI explanations and a remote-cloud deployment are optional future extensions
and are not implemented.

[^wilson]: NIST, [Confidence intervals for proportions](https://itl.nist.gov/div898/handbook/prc/section2/prc241.htm).
[^multipass]: Canonical, [Multipass command reference](https://canonical.com/multipass/docs/latest/reference/command-line-interface/) and [targeted deletion](https://canonical.com/multipass/docs/latest/reference/command-line-interface/delete/).

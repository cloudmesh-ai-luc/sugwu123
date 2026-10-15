# SPORTSSTATS Application

The [solo SPORTSSTATS project](../project.md) uses Python's standard library, SQLite, a JSON API, and a dashboard. Python 3.12+ is required; the application needs no pip packages or paid API. The current historical dataset has **team totals**. Real player statistics are not supplied. The project name is SPORTSSTATS; its Python package stays `sports`, so the existing commands still work.

## Real-Data Midterm Demo

From the repository root:

```bash
make -C sports test
make -C sports history
make -C sports model
make -C sports historical-serve
```

Open <http://127.0.0.1:8000>. Stop with Control-C. The importer downloads approximately 18 MB of pinned FiveThirtyEight data, verifies its SHA-256, and selects the NBA 2014–15 regular season: 2,460 team-game rows, 1,230 games, 30 teams. It keeps both teams' views and marks each aggregate explicitly. Data is CC BY 4.0, attributed to FiveThirtyEight, with original game information attributed there to Basketball-Reference. [Source description](https://github.com/fivethirtyeight/data/tree/master/nba-elo) · [License](https://github.com/fivethirtyeight/data#license).

The source revision and checksum are constants in `history.py`. Raw CSV and SQLite files remain in ignored `sports/data/`. The separate database is `sports/data/history.sqlite3`. Skip `history` after a successful import; it refuses to overwrite existing observations. Only use `python3 -m sports.history --season 2015 --replace` after explicitly deciding to replace that historical dataset.

```bash
python3 -m sports --db sports/data/history.sqlite3 options
python3 -m sports --db sports/data/history.sqlite3 analyze --team CHI --threshold 100.5
python3 -m sports --db sports/data/history.sqlite3 model --team CHI --threshold 100.5
curl --fail http://127.0.0.1:8000/api/health
curl --fail --get http://127.0.0.1:8000/api/model \
  --data-urlencode "team=CHI" --data-urlencode "threshold=100.5"
```

The server must be started with the historical database to produce these results. Expect 82 Chicago games, 43 strictly above 100.5 points, and 72 matched model-evaluation games. Exact results and provenance appear in [aggregate evidence](../project/evidence/nba2015-summary.json).

## Synthetic Player Demo

The original demonstration remains available in a separate database:

```bash
make -C sports demo
make -C sports analyze
make -C sports serve
```

It creates 144 fictional player observations across 36 games, four teams, and eight players. It uses `sports/data/sports.sqlite3`; it does not establish real sports accuracy. Skip `demo` if the database already exists. Replacement requires an explicit `--replace`. Do not run both servers on the same port simultaneously.

## CLI, API, and Custom Imports

The CLI supports `options`, `analyze`, `model`, `import`, `demo`, and `serve`. `GET /api/options` returns filters/provenance; `/api/analyze` and `/api/model` accept `team`, optional `player`/`opponent`, and `threshold`. Unknown filters and invalid thresholds return HTTP 400. Without a player filter, each team game counts once. The historical dashboard hides aggregate markers from the player selector.

For another dataset, obtain explicit usage rights first and prepare these CSV columns:

```text
game_id,date,team,opponent,player,points,team_score,opponent_score
```

Dates use `YYYY-MM-DD`, scores are nonnegative integers, game IDs are consistent for both sides, and player identifiers must be unique within a game. Conflicting scores and duplicate observations are rejected. Missing player records are not treated as zero. Example syntax, with the placeholder values replaced by a real source and rights statement:

```bash
python3 -m sports --db sports/data/custom.sqlite3 import /absolute/path/to/history.csv \
  --source "https://actual-source.example/data" --rights "Actual license or permission"
```

A supplied rights string records provenance; it does not automatically establish permission. Imports validate before replacement, and existing observations require an explicit `--replace`.

## Probability and Model Evaluation

The event is `points > threshold`. The historical rate uses selected games; the 95% Wilson interval describes uncertainty under binomial assumptions, which sports dependence and selection can violate. The original historical-only evaluation begins after five earlier games, with probability `(prior_events + 1) / (prior_games + 2)`.

The model comparison uses online logistic regression: intercept, prior five-game mean, and prior game points, with fixed 20-point scaling relative to the threshold. Learning rate is 0.05. It trains after five prior games and scores after ten. Prediction occurs before the date's update; same-day outcomes cannot leak into their forecasts. **Use the matched model comparison**, not the older five-game-warmup panel, to compare methods.

On the same 72 Chicago evaluation games, Brier scores are logistic **0.2533**, historical rate **0.2572**, constant 50% **0.2500**. Lower is better. The classifier does not beat the constant forecast here. Filtering, threshold selection after viewing results, one season, and a single team limit generalization. No held-out multi-season advantage is claimed.

## Dedicated Multipass VM

On a Mac with Multipass and enough resources for Ubuntu 24.04, 2 CPUs, 2 GiB RAM, and 10 GB disk:

```bash
make -C sports vm-deploy
make -C sports vm-status
make -C sports vm-stop
make -C sports vm-start
```

The existing automation transfers source, runs guest tests, preserves an existing default database, seeds synthetic data on a fresh deployment, and enables systemd on port 8000. **It still serves the synthetic/default database.** It does not automatically import the new historical source or switch the service to `history.sqlite3`. Do not describe a source redeployment alone as historical-model deployment.

`NAME=sports-another-demo` selects another dedicated project VM. Only `sports-` names are accepted. Original [October 1 evidence](../project/vm-deployment.md) shows 23 guest tests then, deployment, stop/start, and 144 synthetic rows after recovery. The earlier October 15 build passed 34 tests on the Mac. The AWS-plan update has preparation-environment verification; the current historical-data demo and VM service still need Mac checks.

## Three-Cloud cmx Adapter

```bash
python3 -m sports.cloud plan --cloud multipass
python3 -m sports.cloud plan --cloud chameleon
python3 -m sports.cloud plan --cloud aws
```

Plans do not execute commands. Selected targets are Multipass, Chameleon KVM@TACC, and Amazon EC2; AWS uses the name `SPORTSSTATS`. Google remains an optional plan, separate from the selected three. Use the instructor's current dev2 and applicable Chameleon feature work. The audited start syntax creates a VM and is not an existing-VM resume operation.

Once source and the historical database really exist in `~/sports-project` on a configured target:

```bash
python3 -m sports.cloud smoke --cloud aws --name SPORTSSTATS
```

This runs a guest analysis via `cmx vm run` and requires a valid success JSON payload with positive row/evaluation counts. A plain error string cannot pass. The adapter does not provision or install remote applications. The AWS Free plan and $100 credits were observed. Live cmx results, remote deployments, provider credentials, and passphrase-protected keys remain unverified. The audited AWS provider has unresolved initialization/method issues. A console launch alone does not complete cmx integration. Do not run the printed start command on an already-created VM. [AWS setup](../project/aws-setup.md) gives the current settings. [Current status](../project.md) and [checklist](../project/midterm-checklist.md) describe the outstanding work.

## Verification and Acknowledgment

The current 34-test suite includes storage/statistics, leakage, importer fixtures, real HTTP CLI/API consistency, deployment safeguards, and cloud command/result contracts. [October 15 log](../project/evidence/oct15-verification.txt) records preparation-environment output. It is not a live-cloud test log. [Mac evidence](../project/evidence/mac-oct15.md) records the separate 34-test screenshot for the earlier October 15 build.

OpenAI Codex substantially assisted with implementation, tests, research, and documentation. [AI usage](../project/ai-usage.md) records extent and limitations; [costs](../project/costs.md) covers paid services and open alternatives. Student review and rehearsal remain necessary.

# SPORTSSTATS Presentation Notes

Open root `project.md` for the instructor's review. The slides are optional. This suggested five-to-seven-minute pace is for practice; it is not an instructor-set time limit. Spoken notes can use first person; the report stays in third person.

## Opening

“My project is called SPORTSSTATS. It looks at basketball scores and how often a team passes a points target. It has a terminal command, an API, and a dashboard. The current version adds real NBA team data and a small machine-learning model.”

## Data

“The data comes from FiveThirtyEight and has a CC BY 4.0 license. The import uses the 2014–15 NBA regular season. There are 1,230 games and 30 teams. Each game has a row for each team, so there are 2,460 rows. These are team scores, not real player statistics. The older player demo uses made-up data.”

## Model and Live Demo

“The question is whether Chicago scores more than 100.5 points. The model uses the previous game and the average of the five games before it. It makes each prediction before seeing that day's result. All three methods are compared on the same 72 games.”

Run these from the repository root only after the historical import has succeeded:

```bash
python3 -m sports --db sports/data/history.sqlite3 model --team CHI --threshold 100.5
make -C sports historical-serve
```

For a local server, open <http://127.0.0.1:8000>. The working AWS dashboard uses the existing Mac SSH tunnel at <http://127.0.0.1:8001>. Keep both AWS Terminal tabs open. Keep CHI, Team total, All opponents, and threshold 100.5. Show the 82-game history, then the separate 72-game machine-learning comparison. If the live demo fails, label the aggregate JSON as saved evidence.

“Chicago passed the target in 43 of 82 games, about 52%. The model's Brier score is 0.2533. The simple 50% forecast scores 0.2500. A lower score is better, so the model did not beat that simple forecast. One team and one season are not enough to claim it predicts future games well.”

Brier means the average squared gap between a probability and the actual result, recorded as zero or one. Always predicting 0.5 gives 0.25 for every outcome. The older historical-only panel starts scoring after five games; use the separate model panel for the fair three-method comparison.

## Cloud Computing and DevOps

“The three chosen clouds are Multipass, Chameleon KVM@TACC, and AWS. Multipass is local, Chameleon is OpenStack, and AWS is the public cloud. The October 1 screenshots show the older local app running and recovering after a restart. The October 15 Mac screenshot shows 34 passing tests for the earlier build.”

"The app is running on an Ubuntu AWS instance. It passed all 34 tests there, and the historical dashboard opened through an SSH tunnel. The account showed $100 in credits this morning; I still need to check current costs and billing alarms. The updated Multipass and Chameleon app and the full cmx checks are still open. The working AWS app uses SSH. The class tool's AWS provider has separate code issues."

“DevOps is the repeatable setup and checking: scripts, tests, Git, a systemd service, and a pinned data download. The dataset checksum helps detect a changed download. Data files and keys stay out of Git.”

Only replace these pending statements with results actually observed before the talk.

## Class Contribution

"The old PR was too large and had conflicts. It is closed and was not merged. Two smaller fixes are prepared in separate branches. One fixes Google driver setup and passes seven focused tests. The other fixes a key-scan error seen today and passes two tests using temporary keys. Neither is published. Only one would be submitted at a time, after review."

“The instructor asked for current upstream code, existing tests to stay, shared hostlist tools to be reused, one provider per PR, separate docs, and one PR at a time. The next submission needs another check against the latest dev2.”

## AI Use and Cost

“OpenAI Codex helped a lot with code, tests, research, running the experiment, and drafting the report and slides. The sports project idea already existed. The AI-use file explains what help was used and what still needs checking. I need to understand and review this work before presenting it.”

“The application does not call a paid AI API. The AWS launch screen showed $0.0104 per compute hour. Fifteen minutes is about $0.0026 before disk, IP, and other costs. Credits can run out. Local Python, SQLite, and Multipass are alternatives that avoid a public VM bill.”

## Remaining Work

"The remaining items are the full live model comparison, complete key checks, reviewed publication, updated local and Chameleon results, cmx automation, and confirmation of project and cloud approval. The next model check should use more seasons and teams with settings chosen before looking at results. Live NBA data will come later."

## Questions to Practice

| Question | Plain answer |
| --- | --- |
| Why this model? | It is a small classifier for a yes/no event and runs on CPU. It can be compared with simple forecasts. |
| Why 82 games versus 72? | The history uses all games. The evaluation skips ten games to build prior history. |
| How is future information kept out? | Inputs use earlier games. Each day's predictions happen before that day's results update the model. |
| What does the interval mean? | It shows uncertainty in the historical rate under assumptions. It does not guarantee the next game's outcome. |
| Are there real player stats? | No. The real data is team totals; the player demo is synthetic. |
| Is the contribution merged? | No. The old PR is closed; the smaller fix is prepared locally. |
| Did AI do all the work? | State the actual assistance. Do not claim the generated changes were written without AI. |

Before the talk, read `sports/history.py`, `sports/model.py`, `sports/cloud.py`, and their tests. Practice explaining one prediction and its later update. Correct any statement that is not supported by the actual results.

Acknowledgment: OpenAI Codex drafted these notes in simpler words. They still need student review and practice.

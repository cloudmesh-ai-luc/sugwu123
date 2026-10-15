# Sports Midterm Presentation Notes

Use root `project.md` as the main review artifact. The optional slides summarize it. This five-to-seven-minute rehearsal is a suggested pace, not an instructor-specified time limit.

## Opening: 30 Seconds

“This solo project analyzes basketball scoring thresholds. The current application stores validated observations, exposes the same analysis through a CLI and API, and uses a dashboard to show trends and uncertainty. The current experiment adds real team data and a small chronological classifier to the earlier synthetic player demo.”

## Data and Method: 60 Seconds

“The source is FiveThirtyEight's historical NBA data, with an explicit CC BY 4.0 license and original game information attributed to Basketball-Reference. The pinned 2014–15 regular-season import contains 2,460 team-game rows. Both teams have a view of each game. These are team totals, not real player statistics.”

“The selected question is whether Chicago exceeds 100.5 points. The model uses only the previous game and the prior five-game mean, scaled relative to the threshold. Each prediction is made before learning that date's result. Evaluation begins after ten earlier games, and all three comparison methods use the same 72 games.”

## Demonstration: 90 Seconds

From the repository root, after tests and import have succeeded:

```bash
python3 -m sports --db sports/data/history.sqlite3 model --team CHI --threshold 100.5
make -C sports historical-serve
```

Open <http://127.0.0.1:8000>. Keep CHI, Team total, All opponents, threshold 100.5. Point to the 82-game historical sample and then the separate 72-game machine-learning comparison. The older baseline panel has a five-game warmup and must not be used for the matched three-method comparison. The report's aggregate JSON is a fallback if the live demo fails; call it saved evidence rather than a live run.

“Chicago exceeded the threshold in 43 of 82 games. The historical rate is 52.44%, with a wide Wilson interval. For the 72-game chronological evaluation, logistic Brier is 0.2533, historical-rate Brier is 0.2572, and constant 50% is 0.2500. Lower is better. The classifier did not beat the constant forecast. That limits the claim; it does not invalidate the measured software workflow.”

## Cloud and DevOps: 60 Seconds

“The existing native Multipass deployment creates a dedicated Ubuntu VM, transfers source, runs guest tests, and sets up systemd. Original October 1 evidence shows 23 guest tests, restart, and a healthy service with 144 synthetic rows. The updated application has 34 passing preparation-environment tests; that is a different environment and version.”

“The three selected targets are Multipass, Chameleon KVM@TACC, and Google Compute Engine. A cmx adapter prints actual command plans and validates the JSON result of a guest analysis on an already deployed VM. Chameleon and Google deployment, credentials and live results remain incomplete. Those cloud plans are not deployment evidence.”

## Contribution and AI Use: 60 Seconds

“The earlier PR #11 is closed and unmerged. The instructor requested current upstream code, preserved tests, reused hostlist utilities, one provider per PR, separate documentation, and one PR at a time. The prepared successor changes only Google driver initialization, a focused test file, and necessary Google fixture/assertion updates in two existing test files. Seven Google-focused tests pass without calling Google; full lifecycle validation is still needed.”

“OpenAI Codex provided substantial help with code, tests, research, experiments, report writing, and slides. The sports project idea already existed. The AI-use document explains the extent, failures, and checks. The application does not call a paid LLM API. Student understanding and live cloud evidence cannot be replaced by generated text.”

## Issues and Next Measurement: 30 Seconds

“Outstanding work includes instructor approval/selection confirmation, today's Mac key checks, publishing the prepared changes, testing the updated local demo, and reproducing the same result on the two remote clouds. The next modeling step is a predefined evaluation on more seasons and teams rather than tuning against this result.”

## Questions to Practice

| Likely question | Explanation to understand |
| --- | --- |
| Why logistic regression? | A small transparent binary classifier fits the above-threshold event and runs on CPU without a paid inference service. It is compared with simple baselines rather than assumed useful. |
| What is a Brier score? | Average `(predicted probability − outcome)^2`, where outcome is 0 or 1. Constant 0.5 always gives 0.25. |
| Why 82 versus 72? | Historical description uses all games; model scoring skips the first ten as prior history. |
| What prevents leakage? | Features contain earlier results only; prediction precedes the date's update. Tests change future/same-day scores and check earlier forecasts stay unchanged. |
| Is the Wilson interval a prediction interval? | No. It concerns the historical frequency under binomial assumptions, with dependence and selection limitations. |
| Is the real dataset player-level? | No. It contains team scores. Synthetic data exercises player UI behavior. |
| Why three clouds? | Local development, an OpenStack reproduction, and a public-cloud CPU run satisfy the required categories; live completion remains to be demonstrated. |
| Has the contribution merged? | No. PR #11 is closed/unmerged; the focused Google successor is prepared, not published. |
| What did the student write without AI? | Only actual personal work should be claimed. The prepared changes received substantial AI implementation and writing assistance. |

Before presenting, read `sports/history.py`, `sports/model.py`, `sports/cloud.py`, and the new tests. Run the commands and explain at least one model prediction/update in plain language. Remove or correct any claim that cannot be supported.

Acknowledgment: OpenAI Codex drafted these rehearsal notes. They are preparation material; they do not certify that student review or understanding has occurred.

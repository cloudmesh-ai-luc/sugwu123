# October 15 Midterm Checklist

The official [Week 7 assignment](https://cloudmesh-ai.github.io/cloudmesh-ai-lecture/lecture/assignments/assignments/) requires three clouds, current cmx branches, small PRs, a contribution summary, and an in-class project review. Slides are optional. Root `project.md` is the review document. The student specified a 4:15 pm presentation today.

| Item | Current evidence | Required action |
| --- | --- | --- |
| Progress report, third person, solo scope | Root report rewritten around actual implementation/results | Review and publish prepared changes |
| Cloud Computing, DevOps, AI, Issues | Explicit sections in root report | Explain each connection during review |
| Permitted real data and chronological evaluation | Pinned CC BY 4.0 NBA import; exact aggregate results | Reproduce on Mac and explain the limitations |
| Local software verification | 34 tests pass in preparation environment | Run the updated suite on Mac |
| Local VM automation | October 1 deployment and stop/start recovery screenshots | Updated historical-model deployment still unverified |
| Three clouds and cmx | Multipass/Chameleon/Google roles and command adapter | Account/provider setup and live remote deployment remain incomplete |
| Small contribution | Google initialization plus one focused test file; four tests pass | Refresh dev2; review; submit only this PR first |
| AI-use MD/slide | AI usage document records substantial assistance | Review for accuracy and present it |
| Paid-service appendix and open alternatives | Cost appendix with estimate and prerequisites | Verify actual benefits/billing before any paid run |
| SSH checks today | Instructor requires two cmx key commands on actual Mac | Run them privately; resolve keys lacking passphrases |
| Instructor project/cloud approval | No explicit approval found in reviewed evidence | Confirm with instructor; do not mark approved without evidence |
| GitHub publication | Write denied to integration | Apply prepared branch changes and push with working Mac access |

## Mac Rehearsal

After applying the prepared changes, from the repository root:

```bash
python3 --version
make -C sports test
make -C sports history
make -C sports model
make -C sports historical-serve
```

Python 3.12+ is required. Skip `history` if `sports/data/history.sqlite3` already exists. Do not add `--replace` without deciding to replace that dataset. Open <http://127.0.0.1:8000>, select CHI, leave Player at Team total, and keep threshold 100.5. Expect 82 selected games, 43 above threshold, and 72 matched model-evaluation games. Stop the server with Control-C.

In the environment containing the instructor's latest cmx, run:

```bash
cmx key scan
cmx key github list
```

Follow Piazza [#124](https://piazza.com/class/mt5rkdsycb31c3/post/124): GitHub/cloudmesh keys need passphrases and ssh-agent/Keychain support. Inspect results locally; do not post private keys, passwords, or detailed security inventory publicly. These checks were not run on the student's Mac by this preparation session.

## Presentation Sequence

1. Open root `project.md`; describe the existing sports problem and current milestone.
2. Show the real source/license and team-total scope.
3. Run CLI model output, then show the matching dashboard comparison.
4. Explain why lower Brier is better and why 0.2500 beats the model's 0.2533 here.
5. Separate old Mac evidence, current preparation tests, and unverified remote clouds.
6. Show the single-provider PR scope and instructor-feedback response.
7. Present `project/ai-usage.md`; identify substantial assistance and review responsibility.
8. State unresolved issues and the next measured experiment.

[Presentation notes and Q&A](presentation-notes.md) provide a short rehearsal script. This checklist records evidence, not a guarantee that all grading requirements are complete.

Acknowledgment: OpenAI Codex drafted and checked this checklist against current course sources. Student review and Mac/cloud checks remain outstanding.

# October 15 Midterm Checklist

The official [Week 7 assignment](https://cloudmesh-ai.github.io/cloudmesh-ai-lecture/lecture/assignments/assignments/) requires three clouds, current cmx branches, small PRs, a contribution summary, and an in-class project review. Slides are optional. Root `project.md` is the review document. The student specified a 4:15 pm presentation today.

| Item | Current evidence | Required action |
| --- | --- | --- |
| Progress report, third person, solo scope | Root report rewritten around actual implementation/results | Review and publish prepared changes |
| Cloud Computing, DevOps, AI, Issues | Explicit sections in root report | Explain each connection during review |
| Permitted real data and chronological evaluation | Pinned CC BY 4.0 NBA import; exact aggregate results | Reproduce on Mac and explain the limitations |
| Application verification | October 15 screenshots show 34 passing tests on Mac and 34 on AWS | Rerun after applying any code update |
| Local VM automation | October 1 deployment and stop/start recovery screenshots | Updated historical-model deployment still unverified |
| Three clouds and cmx | AWS historical dashboard works through SSH; selected targets are Multipass/Chameleon/AWS | Check updated local/Chameleon guests and actual cmx operations |
| Small contribution | Separate Google and key-scanner fixes prepared with focused tests | Refresh dev2; review one candidate; submit one PR at a time |
| AI-use MD/slide | AI usage document records substantial assistance | Review for accuracy and present it |
| Paid-service appendix and open alternatives | AWS appendix with observed credits and compute estimate | Verify required billing alarms; check balance and costs |
| SSH checks today | Both commands attempted; protected keys loaded into agent; scanner bug and missing gh found | Finish the GitHub list; keep scanner evidence private and report the bug accurately |
| Instructor project/cloud approval | No student entry found in the reviewed Piazza #86 record | Confirm Multipass/Chameleon/AWS selection and formal project approval |
| GitHub publication | Default main still shows the older report | Review each prepared change before publishing with working Mac access |
| Full environment automation | Local Multipass script exists; remote setup is incomplete | Finish non-interactive remote deployment and actual cmx verification |
| OpenStack cleanup | Instructor requires KVM@TACC and careful resource use | Use the smallest suitable VM; shelve/delete when idle |

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

Follow Piazza [#124](https://piazza.com/class/mt5rkdsycb31c3/post/124#): GitHub/cloudmesh keys need passphrases and ssh-agent/Keychain support. Demonstrate both command outputs in class, or show the instructor a local file containing them. Keep detailed outputs outside public Git. The Mac scanner prompted for a protected key and still reported "No"; an isolated regression test reproduced this upstream bug. The GitHub list failed because `gh` was missing. Neither result should be presented as a completed successful check.

## Presentation Sequence

1. Open root `project.md`; describe the existing sports problem and current milestone.
2. Show the real source/license and team-total scope.
3. Run CLI model output, then show the matching dashboard comparison.
4. Explain why lower Brier is better and why 0.2500 beats the model's 0.2533 here.
5. Show the working AWS dashboard; distinguish it from older VM evidence and pending cmx/Chameleon results.
6. Explain the instructor's PR feedback and show only one focused candidate at a time.
7. Present `project/ai-usage.md`; identify substantial assistance and review responsibility.
8. State unresolved issues and the next measured experiment.

[Presentation notes and Q&A](presentation-notes.md) provide a short rehearsal script. This checklist records evidence, not a guarantee that all grading requirements are complete.

Acknowledgment: OpenAI Codex drafted and checked this checklist against course sources. Student review, complete key checks, and the remaining cloud checks are still needed.

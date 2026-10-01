# Midterm Preparation Checklist

The published [syllabus](https://cloudmesh-ai.github.io/cloudmesh-ai-lecture/lecture/01.1-syllabus/)
tentatively lists **October 15, 2026** for a project review, programming assignment
review, and review of class contributions. Confirm any schedule changes announced
in class. The syllabus permits working individually.

The [project guidelines](https://cloudmesh-ai.github.io/cloudmesh-ai-lecture/lecture/assignments/overview/)
require instructor approval, a non-trivial application, automated VM/container
management, CLI/API access, and reproducibility. The list below is a preparation
plan based on those requirements, not a separately published midterm grading rubric.

| Requirement or preparation task | Current evidence | Next action |
| --- | --- | --- |
| Solo project and coherent scope | Sports proposal and individual progress report | Explain the selected basketball milestone |
| Formal instructor approval | Not documented | Confirm approval and record its date/context |
| Non-trivial statistical application | Threshold rates, uncertainty, chronological baseline evaluation | Run a documented real-data experiment |
| CLI/API access and justified GUI | Shared CLI/API analysis; dashboard for trends and intervals | Demonstrate both CLI and dashboard |
| Automated VM management | Dedicated Multipass deployment succeeded; service healthy | Verify stop/start persistence |
| Reproducible results | 23 tests passed in preparation environment and in the deployed guest | Retain deployment evidence and demonstrate the app from the Mac |
| Permitted data, no raw data in Git | Generated demo and ignore rules; import provenance fields | Select a licensed/public-domain dataset and retain it outside Git |
| Coursework and contribution review | Week 1–5 links and upstream PR #11 | Resolve or clearly report remaining Week 5 failures and participation status |

## Before the Review

- [x] Connect the prototype to the original sports objectives.
- [x] Document that this is a solo project.
- [x] Provide application tests, CLI/API access, and source-based demo generation.
- [x] Prepare deployment automation and run it on the Mac.
- [x] Publish the prototype and reports to the class repository.
- [ ] Confirm formal instructor approval.
- [ ] Import a permitted historical dataset with recorded source and rights.
- [ ] Evaluate that dataset chronologically and explain uncertainty and bias.
- [x] Run the sports VM deployment and retain a real health response/screenshot.
- [ ] Verify the dashboard and API from the Mac browser/terminal.
- [ ] Verify database persistence after stopping and starting the project VM.
- [x] Update the progress report with the observed deployment results.
- [ ] Review course/programming concepts and class contributions for the midterm.

## Host Verification

The [October 1 deployment screenshot](vm-deployment.md) records a successful
guest deployment, 23 passing guest tests, and a healthy service. Dashboard
reachability and stop/start persistence remain unverified.

From the class repository root, retain the host test output separately from the
preparation-environment verification:

```bash
make -C sports test > project/host-verification.txt 2>&1
make -C sports vm-deploy > project/vm-deployment.txt 2>&1
make -C sports vm-status
make -C sports vm-stop
make -C sports vm-start
```

Inspect each command's output and exit status before marking it complete.
Use the printed VM URL to check the dashboard and `/api/health` from the Mac.
After stop/start, compare the same CLI/API analysis and source metadata with the
earlier result. Record the observation rather than assuming persistence.
Do not commit raw data, databases, VM disks, or credentials with these logs.

## Short Demo Sequence

1. Explain the original sports problem and the narrowed points-threshold question.
2. Identify whether the current data is fictional or real; name its source/rights.
3. Show the same player analysis through the CLI and dashboard.
4. Explain sample size, historical rate, uncertainty, and chronological error.
5. Show actual VM deployment evidence and Week 5's remaining issues.
6. Describe the next experiment and optional future extensions.

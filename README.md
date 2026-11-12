# Sydel Ugwu — COMP 388: Cloud, DevOps & AI (`sugwu123`)

Repository for **Sydel Ugwu (`Sugwu123`)** in COMP 388: Cloud, DevOps, and AI at Loyola University Chicago.

- **Documentation Site (MkDocs):** [https://cloudmesh-ai-luc.github.io/sugwu123/](https://cloudmesh-ai-luc.github.io/sugwu123/)
- **Weekly Status Log:** [assignments/STATUS.md](assignments/STATUS.md)
- **Project Progress Report:** [docs/project/project.md](docs/project/project.md)
- **Smoke Test Benchmarks:** [cloudmesh-ai-vm-results/sugwu123/smoke](https://github.com/cloudmesh-ai/cloudmesh-ai-vm-results/tree/main/sugwu123/smoke)

## Project: SPORTSSTATS

**SPORTSSTATS** is a reproducible basketball statistics and probability forecasting platform built with Python, SQLite, a CLI, a FastAPI + Pydantic REST API, and an interactive web dashboard. It evaluates online logistic regression probability forecasts against historical threshold rates and constant baselines using Brier scores on FiveThirtyEight NBA regular-season data.

- **Selected Cloud Targets:** Multipass (Local), Chameleon `KVM@TACC` (OpenStack), and Amazon EC2 / AWS (Public Cloud)
- **Source Package:** [`src/sports/`](src/sports)
- **Configuration:** [`src/sports/config.yaml`](src/sports/config.yaml)

## Quick Start (`Makefile`)

    make install
    make test
    make demo
    make run
    make doc
    make view

## Weekly Assignments (`assignments/week/<date>`)

All weekly coursework is organized by date inside [`assignments/week/`](assignments/week) and tracked in [`assignments/STATUS.md`](assignments/STATUS.md):

| Week | Folder | Highlights |
|---|---|---|
| **Week 11** | [week/nov12](assignments/week/nov12/README.md) | SSH git remotes in `~/work/`, `code .` terminal setup, Jetstream2 LLM in Cline verification, and `cloudmesh-ai-vm` Issue #116 |
| **Week 10** | [week/nov5](assignments/week/nov5/README.md) | `dev3` migration, `test_config.py` (13/13 passed), Python 3.13 annotation fixes, Multipass smoke tests, and `STATUS.md` |
| **Week 9** | [week/oct29](assignments/week/oct29/README.md) | `src/sports/` package layout, root `Makefile`, `pyproject.toml`, MkDocs hub, and Post #169 code review upgrades (FastAPI/Pydantic, `config.yaml`, structured logging) |
| **Week 8** | [week/oct22](assignments/week/oct22/README.md) | `@cloudmesh-ai` and `luc` team onboarding, `cloudmesh-ai-vm-results` access, and Jetstream2 compromised-key protocol |
| **Week 7** | [week/oct15](assignments/week/oct15/README.md) | Midterm report, FiveThirtyEight NBA chronological evaluation (2,460 rows), and 34 passing unit/HTTP tests on macOS and AWS EC2 |
| **Week 6** | [week/oct8](assignments/week/oct8/README.md) | `cmx` cloud adapter (`sports/cloud.py`), GCE driver constructor patch, and NBA dataset import pipeline |
| **Week 5** | [week/oct1](assignments/week/oct1/README.md) | Automated Multipass VM deployment (`sports/vm.py`), systemd service recovery, and 23 guest verification tests |
| **Week 4** | [week/sep24](assignments/week/sep24/README.md) | Jetstream2, Chameleon, and local Makefiles plus initial `SPORTSSTATS` SQLite storage and CLI |
| **Week 3** | [week/sep17](assignments/week/sep17/README.md) | Chameleon and Jetstream VM provisioning and SSH verification (`vms.md`) |
| **Week 2** | [week/sep10](assignments/week/sep10/README.md) | Local macOS development setup, Multipass configuration, and backup workflow (`backup.md`) |
| **Week 1** | [week/sep3](assignments/week/sep3/README.md) | Course onboarding, initial local VM login verification (`local-vm.md`), and project proposal |

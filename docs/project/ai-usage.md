# AI Usage for COMP 388

## Tool, Project Origin, and Extent

OpenAI Codex assisted with the existing solo sports statistics project and coursework. The exact underlying model identifier was not exposed in this session. The student may add the model name shown in the application interface if available; an unverified model name should not be invented.

The sports topic was already present in the repository and conversation before this midterm preparation. AI helped refine the experiment and substantially implement and document the milestone. Assistance went beyond proofreading: it included Python source, tests, cloud-command integration, source research, data conversion, execution of local checks, interpretation, report drafting, and presentation materials. No unsupported percentage of AI-written work is claimed.

## Uses and Checks

| Use | AI contribution | Evidence or review still needed |
| --- | --- | --- |
| Requirements | Read official Week 7 directions, Piazza posts, and upstream PR feedback | Instructor confirmation of project/cloud approval remains open |
| Data | Located an explicitly licensed NBA source; wrote a pinned, checksum-checked importer | Import and provenance inspected; raw data kept out of Git |
| Modeling | Implemented online logistic regression and matched chronological baselines | Leakage tests pass; student explanation and broader evaluation still needed |
| Interfaces | Extended CLI/API/dashboard for model comparison | Local HTTP consistency test passes; current Mac/VM demo still needed |
| Cloud work | Prepared three-cloud plans and a guest smoke-result parser | Live Chameleon/Google operation is not established |
| Contributions | Prepared a small Google constructor fix based on current dev2 | Four mocked constructor tests pass; no live GCP lifecycle claim |
| Writing | Drafted report, costs, notes, and optional slides | Student review and rehearsal still needed |

Example instructions from the student included checking the instructor's requirements, keeping the work aligned with the existing sports project, disclosing AI use for the presentation, and making each PR smaller after reading the instructor's feedback. Follow-up prompts focused on verifying claims and preserving the solo-project scope. These summarize prompt intent rather than inventing a full transcript.

## Helpful Results

AI assistance connected implementation to specific course requirements, kept synthetic and real data separate, and produced executable checks. The experiment also retained an unfavorable result: logistic regression did not beat the constant 50% forecast on the selected 72 games. AI-generated explanations were checked against the actual JSON output.

## Failures and Limits

- Earlier screenshot attachments were unavailable in some exchanges. A missing image could not establish that a command worked. Only accessible originals and observed outputs are cited as evidence.
- Older documents contained stale test counts and unfinished recovery checks. The report now separates October 1 Mac evidence from October 15 preparation-environment results.
- The earlier upstream PR was too broad and had conflicts. Its closed, unmerged status is stated; the successor is limited to one Google issue.
- A Google driver fallback looked usable but did not instantiate Libcloud's actual GCE driver. Focused tests now check the real constructor contract.
- GitHub writes were denied by permissions. A prepared patch is not a published contribution. Cloud plans and mocked tests do not establish live cloud operation.
- Passing software tests do not imply good forecasts. The constant baseline has the lowest measured error.

## Responsibility and In-Class Explanation

Before presenting, the student must review the changes, run the local commands, and be able to explain the dataset license, strict threshold event, chronological split, Brier score, baseline result, and each cloud's status. Student review and independent understanding have not been verified by this AI session. The assistance must be acknowledged when discussing code and documents rather than presenting the generated material as wholly unaided work.

The application does not call an LLM service. Development assistance and the statistical classifier are distinct uses of AI. Paid-service costs and open alternatives are described in the [cost appendix](costs.md).

Sources: Piazza [#111](https://piazza.com/class/mt5rkdsycb31c3/post/111), [#88](https://piazza.com/class/mt5rkdsycb31c3/post/88), [#100](https://piazza.com/class/mt5rkdsycb31c3/post/100), and [#101](https://piazza.com/class/mt5rkdsycb31c3/post/101).

Acknowledgment: This disclosure was drafted with substantial OpenAI Codex assistance and requires the student's review for an accurate account of use.

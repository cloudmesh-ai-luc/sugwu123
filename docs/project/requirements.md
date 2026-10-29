# Midterm Requirements Trace

Rechecked October 15, 2026 against the current Week 7 assignment, project guidelines, Piazza #49, #86, #88, #100–102, #110–111, #118, and #123–126, plus the full instructor thread on PR #11. The newest visible feed item, #127, is a student's request about presentation order; it does not confirm this student's presentation slot. See root [project.md](project.md) for current findings rather than treating this trace as proof of completion.

| Instructor direction | Source | Prepared response / remaining evidence |
| --- | --- | --- |
| One local, one OpenStack, one AWS/Azure/GCP cloud | [Week 7](https://cloudmesh-ai.github.io/cloudmesh-ai-lecture/lecture/assignments/assignments/) | Multipass, Chameleon KVM@TACC, AWS; AWS guest tests and dashboard observed; updated local/Chameleon and three-cloud cmx results remain open |
| Latest dev2; Chameleon feature work where needed | Week 7; [Piazza #123](https://piazza.com/class/mt5rkdsycb31c3/post/123#), [#125](https://piazza.com/class/mt5rkdsycb31c3/post/125#), [#126](https://piazza.com/class/mt5rkdsycb31c3/post/126#) | Remote dev2 still f55d7bd when rechecked; installation/key updates reviewed; refresh again before live work/PR |
| Small PRs and contribution summary | Week 7 and [PR #11](https://github.com/cloudmesh-ai/cloudmesh-ai-vm/pull/11) | Separate four-file Google and two-file key-scanner candidates; one PR at a time; neither published |
| Root project.md, not proposal; slides optional | Week 7 and [Piazza #102](https://piazza.com/class/mt5rkdsycb31c3/post/102) | Root progress report; old nested report now points to it |
| Cloud Computing, DevOps, AI; three-cloud cmx section; Issues | Week 7 | Explicit sections in root report with implementation/live-evidence distinction |
| Third-person midterm/final reports | [Piazza #49](https://piazza.com/class/mt5rkdsycb31c3/post/49) | Third-person report; solo name at top |
| Existing student topic, not LLM-invented project | [Piazza #88](https://piazza.com/class/mt5rkdsycb31c3/post/88) | Existing sports topic retained; AI implementation assistance disclosed |
| AI-use Markdown or slide | [Piazza #111](https://piazza.com/class/mt5rkdsycb31c3/post/111) | project/ai-usage.md and visible slide disclosure |
| Acknowledgment describing amount, purpose and extent | [Piazza #100](https://piazza.com/class/mt5rkdsycb31c3/post/100) | Substantial code/research/writing help acknowledged; no invented percentage/model name |
| Paid services costs and open alternatives appendix | [Piazza #101](https://piazza.com/class/mt5rkdsycb31c3/post/101) | project/costs.md; observed AWS Free plan/$100 credits and separate compute estimate; actual VM charges unverified |
| Demonstrate both key commands or show a local output file; all GitHub/cloud keys need passphrases and ssh-agent | [Piazza #124](https://piazza.com/class/mt5rkdsycb31c3/post/124#) | Both commands attempted; passphrase-protected keys loaded into the agent. Scan has a reproduced upstream bug; GitHub list failed because gh was missing. Successful results remain open; detailed outputs stay private |
| Automated management, CLI/API, reproducibility, permitted data, no raw data/disks in Git | [Project guidelines](https://cloudmesh-ai.github.io/cloudmesh-ai-lecture/lecture/assignments/overview/) | Native VM automation, interfaces, tests, pinned licensed source; remote automation incomplete |
| Billing alarms and responsible OpenStack cleanup | Project guidelines and assignment-page warning | AWS alarms unverified; shelve/delete idle OpenStack VMs; stop alone is insufficient |
| Project/cloud approval and recorded selection | Project guidelines; [Piazza #86](https://piazza.com/class/mt5rkdsycb31c3/post/86#) | AWS fits the public-cloud category; student is absent from the reviewed choice record; approval not confirmed |
| Instructor can inspect the current report | [GitHub main report](https://github.com/cloudmesh-ai-luc/sugwu123/blob/main/project.md) | Main still has the older report; prepared branch updates await student review and publication |

## Presentation Readiness

Piazza #126 was checked again in the afternoon. Its instructor follow-up says the new CLI smoke-test exercise (`make multipass`, `make lima`, `make chameleon` from `pytest/smoke`) is for next week. It is separate from this report's pending live application and three-cloud cmx checks. Do not run resource-changing smoke tests blindly against existing presentation VMs.

The prepared report contains the required sections, real-data method/results, contribution summary, AI disclosure, and cost appendix. The current deck already selects AWS. This is a progress report, not proof that all assignment requirements are complete.

Before claiming completion, confirm the full live AWS model comparison, finish the key checks, review/publish the prepared changes, check billing alarms and approval, and finish automated three-cloud deployments with real cmx results. AWS has 34 passing guest tests and a working historical dashboard. Existing Week 3 Chameleon SSH evidence supports earlier infrastructure work; it does not establish the current SPORTSSTATS experiment there. The written Week 7 assignment is due at 9 am; the student's stated 4:15 pm talk is a separate presentation target.

Acknowledgment: OpenAI Codex researched and drafted this mapping. It records sources and current evidence rather than instructor approval or a grading guarantee.

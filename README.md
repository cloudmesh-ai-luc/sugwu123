# Cloud Computing (COMP 388)
Sydel Ugwu

## Sports Project and Midterm

This is a solo Sports Statistics and Probability Analysis Platform project.

- [Canonical midterm progress report](project.md)
- [Run the application](sports/README.md)
- [AI usage disclosure](project/ai-usage.md) and [cost appendix](project/costs.md)
- [Contribution summary and instructor feedback](project/contributions.md)
- [Midterm checklist](project/midterm-checklist.md) and [rehearsal notes](project/presentation-notes.md)
- [Current aggregate results](project/evidence/nba2015-summary.json) and [34-test preparation log](project/evidence/oct15-verification.txt)
- [Original Mac VM deployment/recovery evidence](project/vm-deployment.md)

The current experiment uses licensed 2014–15 NBA team data. On the same 72 Chicago evaluation games, logistic Brier is 0.2533 versus constant 50% at 0.2500; the classifier does not beat that baseline. The updated suite passes 34 tests in the preparation environment. October 1 Mac evidence covers the earlier synthetic application and 23 guest tests. Live Chameleon/Google work, the updated Mac demo, key checks, publication, and instructor approval remain open.

## Week 7

- [x] Prepare the root progress report with Cloud Computing, DevOps, AI, and Issues sections.
- [x] Prepare the required AI-use document and paid-service/open-alternative appendix.
- [x] Define Multipass, Chameleon KVM@TACC, and Google targets with a concrete cmx adapter.
- [x] Prepare one focused Google provider fix and four passing constructor tests.
- [ ] Complete live three-cloud deployment/evaluation and verify SSH keys on the actual Mac.
- [ ] Refresh dev2, review, and submit the single small upstream PR.
- [ ] Apply and publish the prepared class-repository changes; rehearse the current demo.

Acknowledgment: OpenAI Codex substantially assisted with the new implementation, tests, and midterm materials. Extent, verification limits, and student review responsibility are recorded in the AI-use document.

## Week 5

- [x] Fork, configure, and launch a test VM.
- [x] Prepare repairs and create a verification script.
- [x] Prepare tested info/run/lifecycle repairs, naming checks, and list formats.
- [x] Verify Multipass lifecycle, naming, and list formats on Mac.
- [x] Manually verify `cmx vm ssh` and `cmx vm login` on Mac.
- [x] Record progress and unfinished work.
- [x] Update Multipass provider documentation.
- [ ] Fully validate all commands and naming behavior.
- [x] Submit upstream [PR #11](https://github.com/cloudmesh-ai/cloudmesh-ai-vm/pull/11), now closed and unmerged; see the contribution summary for feedback.
- [ ] Complete individual Piazza participation and peer review.

[Week 5 report](assignments/week5/README.md)

## Week 4

- [x] Assignment W4.1: VM on local machine via Makefile
  - [x] Manage a local VM using Multipass and a Makefile.
  - [x] Support multiple machines by changing the NAME variable.
  - [x] Organize local and cloud Makefiles in separate directories.
  - [x] [Local VM Makefile](assignments/week4/local/Makefile)

- [x] Assignment W4.2: VM on Jetstream 2
  - [x] Install the OpenStack command-line client using pipx.
  - [x] Create and manage a Jetstream 2 VM with a Makefile.
  - [x] Test VM create, list, info, stop, start, and delete commands.
  - [x] Support multiple machines by changing the NAME variable.
  - [x] [Jetstream 2 Makefile](assignments/week4/jetstream/Makefile)

- [x] Assignment W4.3: VM on Chameleon Cloud
  - [x] Install the OpenStack command-line client.
  - [x] Install python-chi.
  - [x] Create and manage a Chameleon VM with a Makefile.
  - [x] Use an active Chameleon reservation flavor for VM creation.
  - [x] Test VM create, list, info, stop, start, and delete commands.
  - [x] Support multiple machines by changing the NAME variable.
  - [x] [Chameleon Makefile](assignments/week4/chameleon/Makefile)

- [x] Assignment W4.4: Review Python
  - [x] Create and use a Python virtual environment.
  - [x] Review pip and pipx.
  - [x] Review functions and __main__.
  - [x] Pass arguments from the command line using Click.
  - [x] Run shell commands using os.system().
  - [x] Run shell commands using subprocess.run().
  - [x] [Python Review](assignments/week4/python/review.py)



## Week 3

- [x] Assignment W3.1: VM on Jetstream
  - [x] Start a VM on Jetstream and follow the tutorial provided.
  - [x] Document the activity with a screenshot of the terminal (800x600).
  - [x] [vms.md](assignments/week3/vms.md)

- [x] Assignment W3.2: VM on Chameleon Cloud
  - [x] Set the preferred time zone in Chameleon.
  - [x] Upload the SSH public key.
  - [x] Explore the portal and develop a plan.
  - [x] Make a reservation not exceeding 1 hour.
  - [x] Start Ubuntu 24.04 using the smallest compatible VM size.
  - [x] Document the activity with a screenshot of the terminal (800x600).
  - [x] [vms.md](assignments/week3/vms.md)

- [x] Assignment W3.3: OPTIONAL: VM on public cloud

- [x] Assignment W3.4: Compare
  - [x] Compare local VM, Chameleon Cloud, and Jetstream 2.
  - [x] [vms.md](assignments/week3/vms.md)

- [x] Assignment W3.5: README.md
  - [x] README updated with Week 3 assignments and links.

- [x] Assignment W3.6: Git from command line
  - [x] Work with a fork
  - [x] git clone
  - [x] git commit -a
  - [x] git commit -m "msg" file
  - [x] git push
  - [x] git pull
  - [x] Create a pull request
  - [x] Accept a pull request
  - [x] Configure Git username, email, and editor
  - [Pull Request](https://github.com/cloudmesh-ai-luc/sugwu123/pull/1)



## Week 2

- [x] W2.1 Google Account and Piazza Account Post Cleanup
- [x] W2.2 GitHub Repository
- [x] W2.3 Backup Your Computer
- [x] W2.4 Local VM
- [x] W2.4 Project Proposal

### Week 2 Assignment Links

- [Backup Your Computer](assignments/week2/backup.md)
- [Local VM](assignments/week1/local-vm.md)
- [VM Login Screenshot](assignments/week1/vm-login.png)
- [Project Proposal](project.md)

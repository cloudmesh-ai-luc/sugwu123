# Week 5 Progress
Sydel Ugwu

This is an individual Multipass contribution to cloudmesh-ai-vm.
The selected local provider supports the solo Sports Statistics and Probability
Analysis Platform. This update records additional work prepared on October 1;
it does not change the earlier verification evidence or imply everything was
finished by the 9 am deadline.

## Completed work

Forked and cloned the tool, created feature/week5-multipass, and opened
[upstream PR #11](https://github.com/cloudmesh-ai/cloudmesh-ai-vm/pull/11).
The original contribution repaired dependencies, List imports, and named-VM
deletion, and documented an Ubuntu 24.04 launch.

The follow-up contribution adds Multipass info and guest execution, resumes
existing stopped or suspended instances, and uses native restart and suspend.
It adds --name without counter increments, automatic naming with collision
avoidance, list formats, typed configuration commands, and managed guest shells.
Inventory failures now propagate instead of being reported as an empty list.
The provider no longer invents a user SSH key path or security-group resources.

Updated the provider guide and manual, added regression tests, and prepared
a disposable verification script. Live verification is recorded below.

## Verification

| Evidence | Result | Scope |
| --- | --- | --- |
| Earlier Mac verification | 8 passed, 3 failed | Actual host log; two passes were native information queries. |
| Updated unit checks | 117 passed | Python 3.12; mocked provider calls and simulated CLI processes. |
| Shell verifier regression cases | 4 passed, included in the 117 | Success, preflight failure, suspend failure, and launch failure. |
| Latest Mac run | 50 passed, 0 failed | [Actual host log](verification-week5.txt); selected scope verified. |
| Manual Mac shell checks | ssh and login passed | Separate guest sessions; hostname, username, and exit verified in the screenshots below. |

The updated checks ran with:

~~~bash
python -m pytest -q tests/unit --ignore=tests/unit/test_vm.py
~~~

The excluded legacy test imports cloudmesh.ai.cmc, a separate package not
declared by the standalone VM project. That integration remains unverified.
The shell verifier's simulated success case completes 50 checks. Two of these
check expected unsupported errors for shelving; they are not working shelving
operations. Simulated tests do not establish that these commands ran on my Mac.

The earlier log identifies three failures: info and run were not implemented,
and start tried to launch an existing name. The earlier import-failure log is
also retained. The two successful native queries in that older attempt do not
prove stopping or deletion.

## Latest Mac verification

Recorded from [verification-week5.txt](verification-week5.txt) at 2026-10-01T13:04:02-05:00.
Actual script summary: **50 passed, 0 failed**.

The required lifecycle, naming, list-format, and inventory-preservation checks passed.
This confirms the script's selected Multipass scope, including expected-error checks.

Interactive CLI mode, daemon reset, CMC integration, remaining CLI gaps,
other providers, and class participation are still separate tasks.
Unsupported shelving checks are not successful shelving operations.

## Manual shell verification

On October 1, I checked both `cmx vm --cloud multipass ssh` and
`cmx vm --cloud multipass login` using the dedicated test VM
`sugwu-week5-shell-1790881861`. In each guest session, `hostname` returned that
VM name, `whoami` returned `ubuntu`, and `exit` returned to my Mac prompt.

- [SSH check screenshot](images/ssh.png), captured at 2:12 pm.
- [Login check screenshot](images/login.png), captured at 2:20 pm.
- [Targeted cleanup screenshot](images/cleanup.png), captured at 2:28 pm.

I then ran `cmx vm --cloud multipass delete sugwu-week5-shell-1790881861`.
It reported successful deletion, and native `multipass list` no longer showed
the test VM. The inventory still listed `sports-midterm`, `week2-vm`, and
`week4-local` as running, and `balmy-bedbug` as stopped.

The guest sessions and deletion output were recorded on my Mac in
[manual-shell-checks.txt](manual-shell-checks.txt). The screenshots also retain
the shell and cleanup results.
These are two manual checks in addition to the 50 automated Mac checks; they
do not change the automated summary to 52. They do not exercise interactive
CLI mode or `ssh-config`.

## Code understanding

Click loads command modules and passes the selected provider and arguments.
clouds.yaml stores the default provider, resource settings, username, counter,
and last-used VM. StateManager persists those values through YamlDB.
Provider methods translate operations into the appropriate backend calls.
Multipass uses subprocess argument lists and JSON inventory; run invokes a
shell inside the guest through multipass exec. Other cloud providers use
interfaces such as Libcloud, whose authentication and capabilities vary.

The existing dynamic CLI, provider classes, and many lifecycle command modules
were already present. This contribution repairs and completes selected methods
rather than claiming that those existing components were newly created.

## Command coverage

| Commands or requirement | Status |
| --- | --- |
| Multipass start, info, run, stop, restart, suspend, delete | Implemented and regression-tested; Verified in the latest Mac log. |
| Automatic naming, --name, persistent counter, list formats | Implemented and regression-tested; Verified in the latest Mac log. |
| Config and provider selection/discovery | Repaired and covered by the script. |
| ssh and login | Managed shells implemented; both manual Mac checks passed with guest identity and exit verified. |
| shelve and unshelve | Explicitly unsupported; Multipass suspension is not OpenStack shelving. |
| Key/security-group inventories | Empty because those cloud registries are not exposed by Multipass. |
| Key/security-group mutation, regions, account, Horizon | Cloud-specific operations outside the local provider capability set. |
| ssh-config and interactive CLI mode | Further implementation/validation remains. |
| Daemon reset | Excluded from disposable tests because it acts on the provider service. |
| Other local providers and remote Libcloud providers | Not selected or live-tested in this contribution. |
| Piazza discussion and peer review | Drafts prepared; posting and links are not confirmed. |

The verification script uses a temporary configuration and three unique test
names. It launches test VMs sequentially, asserts native state and guest output,
checks counter persistence, parses list formats, and compares the original
inventory. Cleanup targets only those test names with delete --purge NAME.
It does not use a global purge. Manual and unsupported features remain visible
instead of being counted as full feature completeness.

## Self-assessment and background

The selected Multipass Mac verification is recorded above.
Full command coverage is not claimed. Interactive CLI mode, the separate CMC
integration, and other providers still need work or validation.

The intermittent editable-install namespace error has not been diagnosed.
A regular installation previously allowed verification to run. More background
on Python namespace packages and setuptools editable installations is still
needed to explain the difference.

The instructor requests discussion on Piazza before implementing missing
commands. A prior discussion link is not recorded, so compliance with that
step is not claimed. The candidate changes and a concrete discussion draft
are available for review. Individual peer participation remains part of this
solo implementation's class contribution.

## Evidence and contribution links

- [Verification launcher](verify_vm.sh)
- [Unit-test output](unit-tests.txt)
- [Earlier Mac retry](verification-retry.txt)
- [Earlier import-failure attempt](verification.txt)
- [Successful original launch](start-retry.txt)
- [Participation drafts and status](participation.md)
- [Proposed PR description](pr-update.md)
- [Code branch](https://github.com/Sugwu123/cloudmesh-ai-vm/tree/feature/week5-multipass)
- [Multipass guide](https://github.com/Sugwu123/cloudmesh-ai-vm/blob/feature/week5-multipass/docs/providers/local/multipass.md)
- [Manual](https://github.com/Sugwu123/cloudmesh-ai-vm/blob/feature/week5-multipass/docs/manual.md)
- [Disposable verifier](https://github.com/Sugwu123/cloudmesh-ai-vm/blob/feature/week5-multipass/tests/bin/verify_multipass_week5.sh)

The latest automated Mac log is retained as verification-week5.txt beside this report.

## Connection to the Sports Project

The [Sports Statistics and Probability Analysis Platform](../../project.md)
uses a backend, SQLite storage, analytics, and a dashboard. VM lifecycle and
guest-command repairs support reproducible hosting and administration of those
components. They do not validate the sports model or replace application tests.

The [sports prototype](../../sports/README.md) already has team/player/opponent
filters, threshold rates, uncertainty intervals, a chronological baseline,
a CLI, and a JSON API. Its deployment uses native Multipass commands on the
separate sports-midterm VM. The Week 5 verifier does not operate on that VM.
Adopting cmx in the sports deployment is a later integration step after live
provider checks.

The sports application's 23 tests are separate from the Week 5 checks.
See the [midterm progress report](../../project/project.md) for application
evidence and remaining sports data, evaluation, and approval tasks.

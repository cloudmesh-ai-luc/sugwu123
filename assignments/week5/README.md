# Week 5 Progress
Sydel Ugwu

This implementation was completed individually.

## Completed work

Forked and cloned cloudmesh-ai-vm and created a feature branch. Added missing dependencies and List imports. Configured Multipass and successfully launched an Ubuntu 24.04 test VM through cmx. Prepared a deletion change that targets only the named VM. Created verify_vm.sh and retained verification logs.

## Verification

Results: 8 passed, 3 failed

The earlier run recorded two successful information queries and nine CLI import failures. Those successful queries do not establish successful stopping or deletion. See the logs for the actual command output.

## Code understanding

Click exposes CLI commands, clouds.yaml stores provider settings and VM state, and provider methods perform the operations. Multipass uses subprocess calls. Remote providers use Libcloud drivers, whose supported features and authentication vary between clouds.

## Self-assessment

Full command coverage and naming-counter behavior remain unverified. Import behavior and failing provider operations need further investigation. Remote Libcloud providers, shelve/unshelve, Piazza coordination, and peer review remain unfinished. Existing CLI commands and provider classes were already present, so this work focused on repairs and validation.

## Evidence

- [Verification script](verify_vm.sh)
- [Latest attempt](verification-retry.txt)
- [Earlier verification](verification.txt)
- [Successful launch](start-retry.txt)
- [Tool fork](https://github.com/Sugwu123/cloudmesh-ai-vm)

## Contribution links

- [Code branch](https://github.com/Sugwu123/cloudmesh-ai-vm/tree/feature/week5-multipass)
- [Updated Multipass guide](https://github.com/Sugwu123/cloudmesh-ai-vm/blob/feature/week5-multipass/docs/providers/local/multipass.md)

- [Upstream PR #11](https://github.com/cloudmesh-ai/cloudmesh-ai-vm/pull/11)

## Background still needed

The intermittent editable-install namespace errors are still unexplained.
Further background on Python namespace packages and setuptools editable
installations is needed to diagnose that behavior.

## Connection to the Sports Project

The [Sports Statistics and Probability Analysis Platform](../../project.md)
needs a backend to ingest sports observations, store them, calculate statistics,
and serve its dashboard. Week 5 supports the VM infrastructure needed to host
those components. Dependency repairs, named-VM deletion, and command verification
help make that infrastructure reproducible and safer to manage.

The [sports prototype](../../sports/README.md) provides the application layer:
SQLite storage, team/player/opponent filters, historical threshold rates,
uncertainty intervals, a chronological baseline evaluation, a CLI, and a JSON API.
Its dedicated VM deployment script uses native Multipass commands while the
recorded cmx provider failures remain unresolved.

The Week 5 result remains **8 passed and 3 failed**, including two native
Multipass queries among the successful checks. Full command and naming coverage
is still unverified. The disposable Week 5 VM was a tool-validation VM; it was
not evidence of a deployed sports application or a validated sports prediction.

This work was performed individually. See the [midterm progress report](../../project/project.md)
for the application evidence and remaining project tasks.

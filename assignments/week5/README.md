# Week 5 Progress
Sydel Ugwu

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

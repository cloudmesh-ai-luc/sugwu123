# Proposed PR update

Title: Fix Multipass lifecycle, guest commands, naming, and list output

The standalone VM CLI previously failed on missing dependencies/imports, and
Multipass verification exposed unsupported info/run calls and a duplicate
launch when starting a stopped VM. This contribution repairs the imports and
dependencies, limits deletion to the named VM, implements information and guest
execution, and resumes existing stopped/suspended instances.

It adds --name without counter increments, collision-aware automatic naming,
JSON/YAML/CSV/table VM exports, typed configuration commands, and managed
Multipass shells. Backend errors propagate instead of becoming empty inventory.
The provider guide and manual describe supported and unsupported capabilities.

Validation: 117 unit checks passed with tests/unit/test_vm.py excluded because
it imports the separate cloudmesh.ai.cmc package. These checks include four
simulated end-to-end verifier scenarios. They are not real VM evidence.
Live Mac verification recorded 50 passed and 0 failed for the selected scope.
The earlier 8-pass, 3-failure log is retained as historical evidence.
Separate manual ssh and login checks both verified the dedicated guest's
hostname, the ubuntu user, and a clean exit to the Mac prompt.
The manual test VM was then deleted by name. Native inventory confirmed its
absence and still listed the four existing VMs, including the running sports VM.

The disposable verifier creates three unique test VMs sequentially, isolates
configuration, asserts states/output/counters, and preserves other VM inventory.
Shelve/unshelve remain unsupported. Interactive CLI mode, ssh-config, daemon
reset, CMC integration, and other providers require separate work or validation.

Evidence:

- [Latest Mac verification](https://github.com/cloudmesh-ai-luc/sugwu123/blob/main/assignments/week5/verification-week5.txt)
- [Unit-test output](https://github.com/cloudmesh-ai-luc/sugwu123/blob/main/assignments/week5/unit-tests.txt)
- [Manual SSH and login results](https://github.com/cloudmesh-ai-luc/sugwu123/blob/main/assignments/week5/README.md#manual-shell-verification)
- [Disposable verifier](https://github.com/Sugwu123/cloudmesh-ai-vm/blob/feature/week5-multipass/tests/bin/verify_multipass_week5.sh)

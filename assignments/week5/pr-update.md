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
The earlier Mac log was 8 passed and 3 failed.
Live Mac verification: 50 passed, 0 failed; selected scope verified.

The disposable verifier creates three unique test VMs sequentially, isolates
configuration, asserts states/output/counters, and preserves other VM inventory.
Shelve/unshelve remain unsupported, and interactive shells, daemon reset,
CMC integration, and other providers require separate validation.

Replace the pending Mac line with the actual new result after retaining the log.

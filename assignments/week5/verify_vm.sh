#!/usr/bin/env bash
# Sydel Ugwu
VM_NAME="sugwu-week5-test"
PASSED=0
FAILED=0

check() {
    local label="$1"
    shift
    printf '\nTesting: %s\n' "$label"
    "$@"
    local result=$?
    if [ "$result" -eq 0 ]; then
        echo "PASS: $label"
        PASSED=$((PASSED + 1))
    else
        echo "FAIL: $label (exit $result)"
        FAILED=$((FAILED + 1))
    fi
}

check "CLI help" cmx vm --help
check "VM listing" cmx vm list vms
check "VM information" cmx vm info "$VM_NAME"
check "Remote hostname" cmx vm run "$VM_NAME" hostname
check "Restart" cmx vm restart "$VM_NAME"
check "Stop" cmx vm stop "$VM_NAME"
check "State after stop" multipass info "$VM_NAME"
check "Start existing VM" cmx vm start "$VM_NAME"
check "Restore using restart" cmx vm restart "$VM_NAME"
check "Delete dedicated test VM" cmx vm delete "$VM_NAME"
check "Final inventory" multipass list

printf '\nResults: %s passed, %s failed\n' "$PASSED" "$FAILED"
[ "$FAILED" -eq 0 ]
